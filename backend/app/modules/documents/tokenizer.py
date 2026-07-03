import tiktoken

class Tokenizer:
    def __init__(self, model_name: str = "cl100k_base"):
        # Default cl100k_base is used by OpenAI text-embedding-ada-002 and text-embedding-3
        self.encoding = tiktoken.get_encoding(model_name)

    def count_tokens(self, text: str) -> int:
        return len(self.encoding.encode(text, disallowed_special=()))

    def truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        tokens = self.encoding.encode(text, disallowed_special=())
        if len(tokens) <= max_tokens:
            return text
        return self.encoding.decode(tokens[:max_tokens])
