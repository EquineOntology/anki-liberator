import http.client
import json

from anki import hooks
from anki.template import TemplateRenderContext, TemplateRenderOutput
from aqt import mw

config = mw.addonManager.getConfig(__name__)
assert config is not None, "Could not load config"

examples = "<examples>\n<example>\n<PROMPT_HTML>\nlediglich\n</PROMPT_HTML>\n<RESPONSE_HTML>\nmerely; only; simply (l~)\n</RESPONSE_HTML>\n<ideal_output>\n<analysis>\nKey elements:\n- Prompt: \"lediglich\"\n- Response: \"merely; only; simply (l~)\"\n\nPossible strategies:\n1. Change question format\n2. Add context with a German sentence\n3. Ask for synonyms\n4. Use the word in a phrase\n\nEvaluation:\n1. Simple change, might not be engaging enough\n2. Provides real-world context and reinforces meaning\n3. Could be too difficult if user is just learning the word\n4. Good option, but less context than a full sentence\n\nReasoning:\nAdding context with a German sentence (option 2) seems most suitable. It maintains the difficulty level, provides practical usage, and allows for deeper understanding of the word in context.\n</analysis>\n\nWhat does <b>lediglich</b> mean in the following sentence?<br />\n<i>Er wollte <div style=\"color:red\">lediglich</div> helfen, aber niemand hat auf ihn gehört.</i>\n</ideal_output>\n</example>\n<example>\n<PROMPT_HTML>\nlediglich\n</PROMPT_HTML>\n<RESPONSE_HTML>\nmerely; only; simply (l~)\n</RESPONSE_HTML>\n<ideal_output>\n<analysis>\nKey elements:\n- Prompt: \"lediglich\"\n- Response: \"merely; only; simply (l~)\"\n\nPossible strategies:\n1. Change question format\n2. Ask for English translation\n3. Use the word in a short phrase\n4. Ask about part of speech\n\nEvaluation:\n1. Simple change, could be effective for breaking pattern\n2. Direct translation, might be too similar to original\n3. Good for context, but might be too complex\n4. Shifts focus from meaning, might be too difficult\n\nReasoning:\nChanging the question format (option 1) is most suitable here. It maintains the same level of difficulty and tests the same knowledge, while breaking the pattern of the original prompt.\n</analysis>\n\nWhat does <b>lediglich</b> translate to?\n</ideal_output>\n</example>\n<example>\n<PROMPT_HTML>\nmerely; only; simply (l~)\n</PROMPT_HTML>\n<RESPONSE_HTML>\nlediglich\n</RESPONSE_HTML>\n<ideal_output>\n<analysis>\nKey elements:\n- Prompt: \"merely; only; simply (l~)\"\n- Response: \"lediglich\"\n\nPossible strategies:\n1. Ask for German translation directly\n2. Provide a paragraph and ask to identify the word\n3. Use synonyms in English and ask for German equivalent\n4. Create a fill-in-the-blank sentence in German\n\nEvaluation:\n1. Too simple, doesn't provide context\n2. Provides rich context and tests comprehension\n3. Could be confusing if synonyms are not well-known\n4. Good for testing, but less comprehensive than a paragraph\n\nReasoning:\nProviding a paragraph and asking to identify the word (option 2) is most suitable. It offers rich context, tests comprehension, and exposes the user to real-world usage of the word, which enhances learning and memory retention.\n</analysis>\n\nHere is a brief paragraph in German. Find the word that means <b>simply</b>:<br />\n<i>Ich wollte lediglich kurz mit ihm sprechen, aber er war leider nicht da. Dann bin ich schnell nach Hause gegangen und habe einfach gewartet. Es war wirklich nicht schlimm, nur ein bisschen nervig.</i>\n</ideal_output>\n</example>\n<example>\n<PROMPT_HTML>\nHow can you distinguish a hawk and a falcon?\n</PROMPT_HTML>\n<RESPONSE_HTML>\n1) Beak: falcons have a notch on their beak called a \"tooth\", hawks have a simple curve<br><br>2) Hunting: typically falcons hunt other birds or bats, whereas hawks hunt rabbits, rats, and small mammals<br><br>3) Speed of flight: falcons are very fast, hawks are much slower<br><br>4) Size: falcons are smaller than hawks, which are generally larger but with shorter wings\n</RESPONSE_HTML>\n<ideal_output>\n<new_prompt>\nWhich of the following characteristics would help you MOST accurately distinguish a falcon from a hawk?\n\n<div style=\"background-color:#f0f0f0; padding:10px; border-radius:5px;\">\nA) Falcons have a notched beak and hunt birds, while hawks have a curved beak and hunt mammals<br>\nB) Falcons are smaller and faster in flight, while hawks are larger with shorter wings<br>\nC) Hawks exclusively hunt rabbits, while falcons only hunt bats<br>\nD) Falcons and hawks have identical physical characteristics and hunting patterns\n</div>\n</new_prompt>\n</ideal_output>\n</example>\n</examples>\n\n"

prompt = "You are an AI assistant specialized in creating varied and effective flashcard prompts for language learning and other educational purposes. Your task is to generate a new prompt that conveys the same meaning as the original but with subtle variations in wording or structure to enhance learning and prevent pattern matching.\n\nYou will be given two inputs:\n\n<prompt_html>\n{{PROMPT_HTML}}\n</prompt_html>\n\nThis contains the original flashcard prompt.\n\n<response_html>\n{{RESPONSE_HTML}}\n</response_html>\n\nThis contains the correct answer or response to the prompt.\n\nTo generate a new prompt, follow these steps:\n\n1. Analyze the content of both the prompt and response HTML.\n2. Identify the key concept or vocabulary being tested.\n3. Generate a new prompt using one or more of the following strategies:\n   a) Change the question format (e.g., \"What does X mean?\" to \"Define X\")\n   b) Add context (e.g., \"What does X mean in this sentence: [example]\")\n   c) Alter the grammatical form (e.g., change verb tenses or use different parts of speech)\n   d) Rephrase the question entirely while maintaining the core concept\n   e) For language learning, consider using different forms of the word, incorporating it into a short phrase or sentence, or asking for synonyms/antonyms\n   f) For concept-based flashcards, approach the concept from a different angle, ask for examples/applications, or request comparisons with related concepts\n\n4. Ensure your new prompt:\n   - Maintains the same level of difficulty as the original\n   - Tests the same core knowledge or skill\n   - Does not introduce new information not present in the original prompt or response\n   - Remains clear and unambiguous\n\n5. Format your output:\n   - Preserve essential HTML formatting (e.g., bold, italic, underline)\n   - Maintain any images or media present in the original prompt\n   - Ensure that any links or references remain functional\n\nWrap your thought process in <analysis> tags. In your analysis:\n- Write down key elements from both the prompt and response HTML.\n- List out possible strategies for generating a new prompt based on the content.\n- Evaluate each strategy's suitability for the given content.\n- Explain your reasoning for choosing the final approach.\n\nProvide your new prompt in well-formatted HTML, preserving any necessary styling or media elements from the original. Make sure the new prompt ONLY is wrapped in <new_prompt> tags."
                

def request_variation(prompt: str, answer: str) -> str:
    conn = http.client.HTTPSConnection("api.anthropic.com")

    headers = {
        "x-api-key": config["anthropic_api_key"],
        "anthropic-version": config["anthropic_api_version"],
        "content-type": "application/json",
    }

    payload = json.dumps({
        "model": config["anthropic_model"],
        "max_tokens": 1000,
        "temperature": config["anthropic_temperature"],
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "<examples>\n<example>\n<PROMPT_HTML>\nlediglich\n</PROMPT_HTML>\n<RESPONSE_HTML>\nmerely; only; simply (l~)\n</RESPONSE_HTML>\n<ideal_output>\n<analysis>\nKey elements:\n- Prompt: \"lediglich\"\n- Response: \"merely; only; simply (l~)\"\n\nPossible strategies:\n1. Change question format\n2. Add context with a German sentence\n3. Ask for synonyms\n4. Use the word in a phrase\n\nEvaluation:\n1. Simple change, might not be engaging enough\n2. Provides real-world context and reinforces meaning\n3. Could be too difficult if user is just learning the word\n4. Good option, but less context than a full sentence\n\nReasoning:\nAdding context with a German sentence (option 2) seems most suitable. It maintains the difficulty level, provides practical usage, and allows for deeper understanding of the word in context.\n</analysis>\n\nWhat does <b>lediglich</b> mean in the following sentence?<br />\n<i>Er wollte <div style=\"color:red\">lediglich</div> helfen, aber niemand hat auf ihn gehört.</i>\n</ideal_output>\n</example>\n<example>\n<PROMPT_HTML>\nlediglich\n</PROMPT_HTML>\n<RESPONSE_HTML>\nmerely; only; simply (l~)\n</RESPONSE_HTML>\n<ideal_output>\n<analysis>\nKey elements:\n- Prompt: \"lediglich\"\n- Response: \"merely; only; simply (l~)\"\n\nPossible strategies:\n1. Change question format\n2. Ask for English translation\n3. Use the word in a short phrase\n4. Ask about part of speech\n\nEvaluation:\n1. Simple change, could be effective for breaking pattern\n2. Direct translation, might be too similar to original\n3. Good for context, but might be too complex\n4. Shifts focus from meaning, might be too difficult\n\nReasoning:\nChanging the question format (option 1) is most suitable here. It maintains the same level of difficulty and tests the same knowledge, while breaking the pattern of the original prompt.\n</analysis>\n\nWhat does <b>lediglich</b> translate to?\n</ideal_output>\n</example>\n<example>\n<PROMPT_HTML>\nmerely; only; simply (l~)\n</PROMPT_HTML>\n<RESPONSE_HTML>\nlediglich\n</RESPONSE_HTML>\n<ideal_output>\n<analysis>\nKey elements:\n- Prompt: \"merely; only; simply (l~)\"\n- Response: \"lediglich\"\n\nPossible strategies:\n1. Ask for German translation directly\n2. Provide a paragraph and ask to identify the word\n3. Use synonyms in English and ask for German equivalent\n4. Create a fill-in-the-blank sentence in German\n\nEvaluation:\n1. Too simple, doesn't provide context\n2. Provides rich context and tests comprehension\n3. Could be confusing if synonyms are not well-known\n4. Good for testing, but less comprehensive than a paragraph\n\nReasoning:\nProviding a paragraph and asking to identify the word (option 2) is most suitable. It offers rich context, tests comprehension, and exposes the user to real-world usage of the word, which enhances learning and memory retention.\n</analysis>\n\nHere is a brief paragraph in German. Find the word that means <b>simply</b>:<br />\n<i>Ich wollte lediglich kurz mit ihm sprechen, aber er war leider nicht da. Dann bin ich schnell nach Hause gegangen und habe einfach gewartet. Es war wirklich nicht schlimm, nur ein bisschen nervig.</i>\n</ideal_output>\n</example>\n<example>\n<PROMPT_HTML>\nHow can you distinguish a hawk and a falcon?\n</PROMPT_HTML>\n<RESPONSE_HTML>\n1) Beak: falcons have a notch on their beak called a \"tooth\", hawks have a simple curve<br><br>2) Hunting: typically falcons hunt other birds or bats, whereas hawks hunt rabbits, rats, and small mammals<br><br>3) Speed of flight: falcons are very fast, hawks are much slower<br><br>4) Size: falcons are smaller than hawks, which are generally larger but with shorter wings\n</RESPONSE_HTML>\n<ideal_output>\n<new_prompt>\nWhich of the following characteristics would help you MOST accurately distinguish a falcon from a hawk?\n\n<div style=\"background-color:#f0f0f0; padding:10px; border-radius:5px;\">\nA) Falcons have a notched beak and hunt birds, while hawks have a curved beak and hunt mammals<br>\nB) Falcons are smaller and faster in flight, while hawks are larger with shorter wings<br>\nC) Hawks exclusively hunt rabbits, while falcons only hunt bats<br>\nD) Falcons and hawks have identical physical characteristics and hunting patterns\n</div>\n</new_prompt>\n</ideal_output>\n</example>\n<example>\n<PROMPT_HTML>\nIn vim, how can I repeat a search in the same (and opposite) direction?\n</PROMPT_HTML>\n<RESPONSE_HTML>\n<code>;</code> repeats in the same direction, <code>,</code> repeats in the reverse direction\n</RESPONSE_HTML>\n<ideal_output>\nGiven a text like: \"Hello world, hello vim, hello search\", demonstrate how <code>;</code> and <code>,</code> work when searching for \"hello\".<br />\nExample workflow: <ol><li>Start at the beginning of the text</li><li>Search for first \"hello\" using <code>/hello</code></li><li>Show what happens when pressing <code>;</code></li><li>Show what happens when pressing <code>,</code></li></ol>\n</ideal_output>\n</example>\n<example>\n<example_description>\nThe output is good because:\n- It doesn't include useless hints\n- It doesn't include \"in Betracht ziehen\" anywhere, which would give the answer away\n</example_description>\n<PROMPT_HTML>\n🇩🇪 in Betracht ziehen (noun-verb combo)\n</PROMPT_HTML>\n<RESPONSE_HTML>\n🇩🇪 to consider (noun-verb combo)\n</RESPONSE_HTML>\n<ideal_output>\n🇩🇪 Complete the following sentence by using the correct form of the verb \"to consider\":\nWir __________ verschiedene Optionen für unser nächstes Projekt.\n</ideal_output>\n</example>\n</examples>\n\n"
                    },
                    {
                        "type": "text",
                        "text": config["anthropic_prompt"]
                    },
                    {
                        "type": "text",
                        "text": f"<prompt_html>{prompt}</prompt_html><response_html>{answer}</response_html>"
                    }
                ]
            }
        ]
    })

    conn.request("POST", "/v1/messages", payload, headers)
    response = conn.getresponse()
    response_json = json.loads(response.read().decode("utf-8"))
    # return response_json

    if "content" in response_json:
        text_blocks = [block["text"] for block in response_json["content"] if block["type"] == "text"]
        formatted_text = "\n\n".join(text_blocks)  # Join blocks with double line breaks for paragraph formatting
        
        new_prompt = formatted_text[formatted_text.find("<new_prompt>"):formatted_text.find("</new_prompt>")]

        return new_prompt if len(new_prompt) > 0 else prompt
    else:
        return prompt


def prepare(output: TemplateRenderOutput, context: TemplateRenderContext) -> None:
    question = output.question_and_style()
    answer = output.answer_and_style().replace(question, "")
    variation = request_variation(question, answer)

    output.question_text = variation
    # output.question_text = f"question: {question} | answer: {output.answer_and_style()} | clean answer: {answer}"

hooks.card_did_render.append(prepare)
