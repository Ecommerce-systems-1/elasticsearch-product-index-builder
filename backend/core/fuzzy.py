    def one_edit_variants(term: str) -> set[str]:
        variants = set()
        for i in range(len(term)):
            variants.add(term[:i] + term[i+1:])  # deletion
            if i < len(term) - 1:  # transposition
                variants.add(term[:i] + term[i+1] + term[i] + term[i+2:])
        return variants