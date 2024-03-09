import uuid
from urllib.parse import unquote_plus

import boto3
from PIL import Image


# https://note.nkmk.me/en/python-pillow-square-circle-thumbnail/
def crop_center(pil_img: Image.Image, crop_width, crop_height):
    img_width, img_height = pil_img.size

    return pil_img.crop(
        (
            (img_width - crop_width) // 2,
            (img_height - crop_height) // 2,
            (img_width + crop_width) // 2,
            (img_height + crop_height) // 2,
        )
    )


def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


def resize_image(file, filename):
    with Image.open(file) as im:
        im = crop_max_square(im)
        im.thumbnail((400, 400))
        im.save(filename, "JPEG")


s3_client = boto3.client("s3")


def lambda_handler(event, context):
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = unquote_plus(record["s3"]["object"]["key"])

        tmpkey = key.replace("/", "")
        download_path = "/tmp/{}{}".format(uuid.uuid4(), tmpkey)
        upload_path = "/tmp/resized-{}".format(tmpkey)

        s3_client.download_file(bucket, key, download_path)
        resize_image(download_path, upload_path)

        s3_client.upload_file(upload_path, bucket, key.replace("/", "-processed/"))
        s3_client.delete_object(Bucket=bucket, Key=key)
