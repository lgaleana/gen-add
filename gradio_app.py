import gradio as gr

import ai_tasks
import code_tasks
import custom_code
from control_flow.main import _run


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


with gr.Blocks() as demo:
    gr.Markdown(
        """
        ## Ad Generator
        Enter an url and the dimensions for an image (eg, 300x600) and get the image and headline for an ad."""
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
                gr.Textbox(
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
                gr.Textbox(
                    ai_tasks.headlines_for_images.PROMPT,
                    label="Instructions",
                    interactive=True,
                )
            with gr.Column():
                headline = gr.Textbox(
                    label="Output: {headline}",
                    lines=20,
                    max_lines=10,
                    interactive=False,
                )

    execute.click(
        get_text_and_images_from_url, inputs=[url], outputs=[text, images]
    ).success(
        get_images_analysis,
        inputs=[images],
        outputs=[image_infos],
    ).success(
        ai_tasks.text_summary.summarize_text, inputs=[text], outputs=[summary]
    ).success(
        ai_tasks.headlines_for_images.get_headline_for_image,
        inputs=[summary, dimensions, image_infos],
        outputs=[headline],
    )

demo.launch()
