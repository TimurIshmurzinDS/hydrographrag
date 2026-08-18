import os
import pickle
import numpy as np
import torch

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class EmbeddingsManager:
    """
    Manages embedding generation and caching for Dense Graph Extraction.

    Device selection is controlled via EMBEDDINGS_DEVICE.

    Recommended benchmark setting:
        EMBEDDINGS_DEVICE=cpu

    This avoids VRAM contention with Ollama generator workers.
    """

    def __init__(
        self,
        model_name="BAAI/bge-m3",
        cache_path="embeddings_cache.pkl",
    ):
        print(
            f"🚀 Загрузка модели эмбеддингов: "
            f"{model_name}..."
        )

        requested_device = os.getenv(
            "EMBEDDINGS_DEVICE",
            "cpu",
        ).strip().lower()

        if requested_device == "auto":
            self.device = (
                "cuda"
                if torch.cuda.is_available()
                else "cpu"
            )

        elif requested_device.startswith("cuda"):
            if not torch.cuda.is_available():
                raise RuntimeError(
                    "EMBEDDINGS_DEVICE requests CUDA, "
                    "but CUDA is not available."
                )

            self.device = requested_device

        elif requested_device == "cpu":
            self.device = "cpu"

        else:
            raise ValueError(
                "Invalid EMBEDDINGS_DEVICE: "
                f"{requested_device!r}. "
                "Expected 'cpu', 'auto', "
                "'cuda', or 'cuda:N'."
            )

        print(
            f"🧠 Embedding device: {self.device}"
        )

        self.model = SentenceTransformer(
            model_name,
            device=self.device,
        )

        self.cache_path = cache_path
        self.entity_cache = {}

        if os.path.exists(
            self.cache_path
        ):
            print(
                "📦 Загрузка закэшированных "
                f"векторов из {self.cache_path}..."
            )

            with open(
                self.cache_path,
                "rb",
            ) as f:
                self.entity_cache = pickle.load(
                    f
                )

            print(
                "✅ Загружено векторов: "
                f"{len(self.entity_cache)}"
            )

    def get_embedding(
        self,
        text: str,
    ):
        """
        Converts a string into an embedding vector.
        """

        if (
            not text
            or not isinstance(
                text,
                str,
            )
            or text.strip() == ""
        ):
            return np.zeros(
                self.model
                .get_sentence_embedding_dimension()
            )

        return self.model.encode(
            [text],
            show_progress_bar=False,
        )[0]

    def compute_similarity(
        self,
        query_vec,
        entity_vec,
    ):
        """
        Cosine similarity between two vectors.
        """

        q = query_vec.reshape(
            1,
            -1,
        )

        e = entity_vec.reshape(
            1,
            -1,
        )

        return cosine_similarity(
            q,
            e,
        )[0][0]

    def find_top_matches(
        self,
        query_text,
        entities_list,
        top_k=5,
    ):
        if not query_text:
            return []

        query_vec = self.get_embedding(
            query_text
        )

        missing_entities = []

        for entity in entities_list:
            eid = entity["id"]
            name = entity.get(
                "name"
            )

            if (
                eid not in self.entity_cache
                and name
                and isinstance(
                    name,
                    str,
                )
            ):
                missing_entities.append(
                    (
                        eid,
                        name,
                    )
                )

        if missing_entities:
            print(
                "⚡ Пакетное вычисление "
                f"векторов для "
                f"{len(missing_entities)} "
                "узлов..."
            )

            texts_to_encode = [
                item[1]
                for item
                in missing_entities
            ]

            embeddings = self.model.encode(
                texts_to_encode,
                batch_size=256,
                show_progress_bar=True,
            )

            for (
                eid,
                _,
            ), emb in zip(
                missing_entities,
                embeddings,
            ):
                self.entity_cache[
                    eid
                ] = emb

            print(
                "💾 Сохранение кэша "
                "на диск..."
            )

            with open(
                self.cache_path,
                "wb",
            ) as f:
                pickle.dump(
                    self.entity_cache,
                    f,
                )

        scores = []

        for entity in entities_list:
            eid = entity[
                "id"
            ]

            if eid in self.entity_cache:
                score = (
                    self.compute_similarity(
                        query_vec,
                        self.entity_cache[
                            eid
                        ],
                    )
                )

                scores.append(
                    (
                        entity,
                        score,
                    )
                )

        scores.sort(
            key=lambda x: x[1],
            reverse=True,
        )

        return scores[
            :top_k
        ]

    def get_cache_size(
        self,
    ):
        return len(
            self.entity_cache
        )