from semantic_router import Route
from semantic_router.encoders import HuggingFaceEncoder

encoder=HuggingFaceEncoder(name="sentence-transformers/all-MiniLM-L6-v2")
faq = Route(
    name="faq",
    utterances=[
        "What is the return policy?",
        "How can I return a product?",
        "I received a damaged product",
        "Item is broken",
        "Product not working",
        "Need refund",
        "How to exchange?",
        "Can I give back item?",
        "Wrong product received",
        "Return process?",
        "Do you accept cash?",
        "Can I pay using cash?",
        "Cash payment available?",
        "Is COD allowed?",
        "Do you take cash as payment?"
    ],
)
sql = Route(
    name="sql",
    utterances=[
        # Price queries
        "I want to buy nike shoes that have 50% discount",
        "Are there any shoes under Rs 5000?",
        "What is the price of puma running shoes?",

        # Size queries
        "Do you have formal shoes of size 9",

        # Brand/sale queries
        "Are there any Puma shoes in sale?",

        # Rating queries  ← ADD THESE
        "Show me shoes with rating above 4",
        "Which shoes have the highest rating?",
        "I want highly rated shoes",

        # Review queries  ← ADD THESE
        "Show shoes with more than 500 reviews",
        "Which products have the most reviews?",
        "Show me popular shoes with many reviews",

        # Filter/sort queries  ← ADD THESE
        "Filter shoes by rating and reviews",
        "Show best rated shoes with high reviews",
        "List all shoes sorted by rating",
    ],
)
routes=[faq,sql]
from semantic_router.routers import SemanticRouter

router = SemanticRouter(encoder=encoder, routes=routes, auto_sync="local")

if __name__ == "__main__":
    print((router("Do you cash as a payment?")).name)
    print(router("All shoes with rating higher than 4 and total reviews greater than 500").name)