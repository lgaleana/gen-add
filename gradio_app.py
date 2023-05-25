import gradio as gr

import ai
import ai_tasks
import code_tasks
import custom_code


def open__get_text_from_url() -> str:
    with open("code_tasks/text_in_url.py") as f:
        return f.read()


def open__get_images_from_url() -> str:
    with open("code_tasks/images_in_url.py") as f:
        return f.read()


def open__get_image_infos() -> str:
    with open("custom_code/image_analysis.py") as f:
        return f.read()


def get_text_and_images_from_url(url):
    return (
        code_tasks.text_in_url.get_text_from_url(url),
        code_tasks.images_in_url.get_images_from_url(url),
    )


def get_images_analysis(images):
    return custom_code.image_analysis.analyze_images(eval(images))


def summarize_text(
    prompt,
    url,
    dimensions,
    text,
    images,
    image_infos,
    summary,
    headline,
):
    return ai_tasks.text_summary._summarize_text(
        prompt,
        url=url,
        dimensions=dimensions,
        text=text,
        images=images,
        image_infos=image_infos,
        summary=summary,
        headline=headline,
    )


def get_headline_for_image(
    prompt,
    url,
    dimensions,
    text,
    images,
    image_infos,
    summary,
    headline,
):
    import json

    output = ai_tasks.headlines_for_images._get_headline_for_image(
        prompt,
        url=url,
        dimensions=dimensions,
        text=text,
        images=images,
        image_infos=image_infos,
        summary=summary,
        headline=headline,
    )
    return output, json.loads(output)["image_url"]


def get_headline_and_prompt(
    prompt,
    url,
    dimensions,
    text,
    images,
    image_infos,
    summary,
    headline,
):
    import json

    output = ai_tasks.headlines_for_ai_images._generate_headline_and_prompt(
        prompt,
        url=url,
        dimensions=dimensions,
        text=text,
        images=images,
        image_infos=image_infos,
        summary=summary,
        headline=headline,
    )
    output_dict = json.loads(output)
    return (
        output,
        output_dict["ai_prompt"],
        output_dict["ai_prompt"],
        output_dict["dimension_to_map"],
        output_dict["dimension_to_map"],
    )


def generate_image(prompt, dimensions):
    return ai.image.urls(prompt, 1, dimensions)[0]


with gr.Blocks() as demo:
    gr.Markdown(
        """
        ## Scrape a website and get an ad
        Enter an url and the dimensions for an image (eg, 300x600).
        <br> A sequence of code and AI tasks will scrape the website and find an image that best fits those dimensions. They will also generate an AI image.
        <br> It's your job to edit either of those images.
        <br> A headline for your ad will also be generated.
        <br> Play around with the AI tasks to get different results. Text inbetween {} are variables that you have access to.
        """
    )

    url = gr.Textbox(label="Input: {url}")
    dimensions = gr.Textbox(label="Input: {dimensions}")
    execute = gr.Button("Run")

    with gr.Box():
        gr.Markdown("Code task")
        with gr.Row():
            with gr.Column():
                gr.Textbox(
                    "write a python function that given an url returns all text in the website",
                    label="ChatGPT-4 prompt",
                )
                with gr.Accordion("Input: {url}", open=False):
                    gr.Code(open__get_text_from_url(), "python")
            with gr.Column():
                text = gr.Textbox(
                    label="Output: {text}", lines=10, max_lines=10, interactive=False
                )

    with gr.Box():
        gr.Markdown("Code task")
        with gr.Row():
            with gr.Column():
                gr.Textbox(
                    "write a python function that given an url returns all images in the website",
                    label="ChatGPT-4 prompt",
                )
                with gr.Accordion("Input: {url}", open=False):
                    gr.Code(open__get_images_from_url(), "python")
            with gr.Column():
                images = gr.Textbox(
                    label="Output: {images}", lines=10, max_lines=10, interactive=False
                )

    with gr.Box():
        gr.Markdown("Custom code: analyze images with Google Vision")
        with gr.Row():
            with gr.Column():
                with gr.Accordion("Input: {images}", open=False):
                    gr.Code(open__get_image_infos(), "python")
            with gr.Column():
                image_infos = gr.Textbox(
                    label="Output: {image_infos}",
                    lines=10,
                    max_lines=10,
                    interactive=False,
                )

    with gr.Box():
        gr.Markdown("AI task: summarize text")
        with gr.Row():
            with gr.Column():
                summary_prompt = gr.Textbox(
                    ai_tasks.text_summary.PROMPT,
                    label="Instructions:",
                    interactive=True,
                )
            with gr.Column():
                summary = gr.Textbox(
                    label="Output: {summary}", lines=10, max_lines=10, interactive=False
                )

    with gr.Box():
        gr.Markdown("AI task: generate headline for image")
        with gr.Row():
            with gr.Column():
                headline_prompt = gr.Textbox(
                    ai_tasks.headlines_for_images.PROMPT,
                    label="Instructions:",
                    interactive=True,
                    lines=20,
                )
            with gr.Column():
                headline = gr.Textbox(
                    label="Output: {headline}",
                    lines=10,
                    max_lines=10,
                    interactive=False,
                )
                headline_image = gr.Image(interactive=False)

    with gr.Box():
        gr.Markdown("AI task: generate headline and prompt for image")
        with gr.Row():
            with gr.Column():
                ai_prompt_prompt = gr.Textbox(
                    ai_tasks.headlines_for_ai_images.PROMPT,
                    label="Instructions:",
                    interactive=True,
                )
            with gr.Column():
                headline_and_prompt = gr.Textbox(
                    label="Output: {headline_prompt}",
                    lines=20,
                    max_lines=20,
                    interactive=False,
                )
                dimension_to_map = gr.Textbox(
                    label="Output: {dimension_to_map}",
                    interactive=False,
                )
                ai_prompt = gr.Textbox(
                    label="Output: {ai_prompt}",
                    interactive=False,
                )

    with gr.Box():
        gr.Markdown("AI task: generate image")
        with gr.Row():
            with gr.Column():
                with gr.Box():
                    ai_image_prompt = gr.Textbox(
                        label="Instructions: {ai_prompt}",
                        interactive=False,
                    )
                    image_dimensions = gr.Textbox(
                        label="Input: {dimension_to_map}",
                        interactive=False,
                    )
            with gr.Column():
                ai_image = gr.Image()

    vars_ = [
        url,
        dimensions,
        text,
        images,
        image_infos,
        summary,
        headline,
    ]

    execute.click(
        get_text_and_images_from_url, inputs=[url], outputs=[text, images]
    ).success(
        get_images_analysis,
        inputs=[images],
        outputs=[image_infos],
    ).success(
        summarize_text,
        inputs=[summary_prompt] + vars_,  # type: ignore
        outputs=[summary],
    ).success(
        get_headline_for_image,
        inputs=[headline_prompt] + vars_,  # type: ignore
        outputs=[headline, headline_image],
    ).success(
        get_headline_and_prompt,
        inputs=[ai_prompt_prompt] + vars_,  # type: ignore
        outputs=[
            headline_and_prompt,
            ai_prompt,
            ai_image_prompt,
            dimension_to_map,
            image_dimensions,
        ],
    ).success(
        generate_image, inputs=[ai_image_prompt, image_dimensions], outputs=[ai_image]
    )

demo.launch()
