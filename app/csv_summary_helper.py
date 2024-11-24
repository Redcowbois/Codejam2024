from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import InferenceClient

client = InferenceClient(api_key="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")


def textgen_summary(prompt):
    messages = [
        {
            "role": "system",
            "content": "You are a summarizer. Your task is to summarize the information that is given to you while keeping it short."
        },
        {
            "role":"user",
            "content": prompt + "."
        }
    ]

    completion = client.chat.completions.create(
        model="Qwen/Qwen2.5-72B-Instruct", 
        messages=messages, 
        max_tokens=1500
    )

    print(completion.choices[0].message.content)


def textgen_csv(prompt):
    messages = [
        {
            "role": "system",
            "content": """You are a semi-colon separated value file generator.
              Your task is to take the relevant information in a text given to you and create 10 semi-colon separated pairs
              of questions and answers."""
        },
        {
            "role":"user",
            "content": prompt + "."
        }
    ]

    completion = client.chat.completions.create(
        model="Qwen/Qwen2.5-72B-Instruct", 
        messages=messages, 
        max_tokens=1500
    )

    print(completion.choices[0].message.content)


textgen_csv("""Bees are winged insects closely related to wasps and ants, known for their roles in pollination and, in the case of the best-known bee species, the western honey bee, for producing honey. Bees are a monophyletic lineage within the superfamily Apoidea. They are currently considered a clade, called Anthophila.[1] There are over 20,000 known species of bees in seven recognized biological families.[2][3][4] Some species – including honey bees, bumblebees, and stingless bees – live socially in colonies while most species (>90%) – including mason bees, carpenter bees, leafcutter bees, and sweat bees – are solitary.

Bees are found on every continent except Antarctica, in every habitat on the planet that contains insect-pollinated flowering plants. The most common bees in the Northern Hemisphere are the Halictidae, or sweat bees, but they are small and often mistaken for wasps or flies. Bees range in size from tiny stingless bee species, whose workers are less than 2 millimetres (0.08 in) long,[5] to the leafcutter bee Megachile pluto, the largest species of bee, whose females can attain a length of 39 millimetres (1.54 in).

Bees feed on nectar and pollen, the former primarily as an energy source and the latter primarily for protein and other nutrients. Most pollen is used as food for their larvae. Vertebrate predators of bees include primates and birds such as bee-eaters; insect predators include beewolves and dragonflies.

Bee pollination is important both ecologically and commercially, and the decline in wild bees has increased the value of pollination by commercially managed hives of honey bees. The analysis of 353 wild bee and hoverfly species across Britain from 1980 to 2013 found the insects have been lost from a quarter of the places they inhabited in 1980.[6]

Human beekeeping or apiculture (meliponiculture for stingless bees) has been practised for millennia, since at least the times of Ancient Egypt and Ancient Greece. Bees have appeared in mythology and folklore, through all phases of art and literature from ancient times to the present day, although primarily focused in the Northern Hemisphere where beekeeping is far more common. In Mesoamerica, the Mayans have practiced large-scale intensive meliponiculture since pre-Columbian times.[5]
""")