import gradio as gr

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


def summarize_text(prompt, url, dimensions, text, images, image_infos, summary):
    return ai_tasks.text_summary._summarize_text(
        prompt,
        url=url,
        dimensions=dimensions,
        text=text,
        images=images,
        image_infos=image_infos,
        summary=summary,
    )


def get_headline_for_image(prompt, url, dimensions, text, images, image_infos, summary):
    return ai_tasks.headlines_for_images._get_headline_for_image(
        prompt,
        url=url,
        dimensions=dimensions,
        text=text,
        images=images,
        image_infos=image_infos,
        summary=summary,
    )


def set_image(headline):
    import json

    return json.loads(headline)["url"]


with gr.Blocks() as demo:
    gr.Markdown(
        """
        ## Scrape a website and get an ad
        Enter an url and the dimensions for an image (eg, 300x600) and get an image from the website and the headline for an ad.
        """
    )
    gr.Markdown("Edit the AI tasks at your convenience.")

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
                    label="Instructions",
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
                    label="Instructions",
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
                headline_image = gr.Image()

    vars_ = [url, dimensions, text, images, image_infos, summary]

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
        outputs=[headline],
    ).success(
        set_image,
        inputs=[headline],
        outputs=[headline_image],
    )

demo.launch()
