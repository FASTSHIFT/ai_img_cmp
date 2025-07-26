# MIT License
#
# Copyright (c) 2025 VIFEX
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import base64
import os
from enum import Enum
from volcenginesdkarkruntime import Ark

prompt_default = "你是一个负责测试穿戴产品的工程师，第一张图是设计稿，第二张图是测试设备图像，两张图像显示内容是否一致？如果一致，请回复“Yes”，否则请回复“No”并说明原因。"


class ThinkingType(Enum):
    DISABLED = "disabled"
    ENABLED = "enabled"
    AUTO = "auto"


parser = argparse.ArgumentParser(description="Compare two images using AI.")
parser.add_argument("--image-design", type=str, required=True, help="Design image path")
parser.add_argument("--image-device", type=str, required=True, help="Device image path")
parser.add_argument(
    "--model", type=str, default="doubao-seed-1-6-250615", help="Model ID to use"
)
parser.add_argument(
    "--thinking",
    type=ThinkingType,
    default=ThinkingType.DISABLED,
    choices=list(ThinkingType),
    help="Thinking type",
)
parser.add_argument(
    "--prompt", type=str, default=prompt_default, help="Custom prompt text"
)

args = parser.parse_args()

api_key = os.getenv("ARK_API_KEY")
if not api_key:
    print("Please set the ARK_API_KEY environment variable.")
    exit(1)

client = Ark(
    api_key=api_key,
)


def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"Image file {image_path} does not exist.")
        exit(1)
    except IOError:
        print(f"Error reading image file {image_path}.")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)


def make_image_url(image_path):
    if not os.path.exists(image_path):
        print(f"Image file {image_path} does not exist.")
        exit(1)

    base64_image = encode_image(image_path)
    _, ext = os.path.splitext(image_path)
    type = ext[1:].lower()
    return f"data:image/{type};base64,{base64_image}"


print(f"image design: {args.image_design}")
print(f"image device: {args.image_device}")
print(f"model: {args.model}")
print(f"thinking: {args.thinking}")
print(f"prompt: {args.prompt}")

image_url_design = make_image_url(args.image_design)
image_url_device = make_image_url(args.image_device)

print(f"Sending images and prompt to model...")

response = client.chat.completions.create(
    model=args.model,
    thinking={
        "type": args.thinking.value,
    },
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"{image_url_design}"},
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"{image_url_device}"},
                },
                {
                    "type": "text",
                    "text": f"{args.prompt}",
                },
            ],
        }
    ],
)

print("\nModel usage:")
print(f"  Total tokens: {response.usage.total_tokens}")
print(f"  Prompt tokens: {response.usage.prompt_tokens}")
print(f"  Completion tokens: {response.usage.completion_tokens}")

if args.thinking != ThinkingType.DISABLED:
    print(f"\nModel thinking: {response.choices[0].message.reasoning_content}")

response_msg = response.choices[0].message.content
print(f"\nModel response:\n{response_msg}")

if response_msg == "Yes":
    print("测试通过")
else:
    print("测试未通过")
