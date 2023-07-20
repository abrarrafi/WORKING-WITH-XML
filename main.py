import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont

def parse_xml_file(xml_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    line_items = root.findall('.//po_line_item')

    question_data = {}
    for line_item in line_items:
        questions = line_item.findall(".//question")
        for question in questions:
            question_id = question.get("question_id")
            question_description = question.get("question")
            if question_id not in question_data:
                question_data[question_id] = question_description

    question_ids = sorted(list(question_data.keys()))

    question_values = []
    for line_item in line_items:
        question_item = {}

        for question_id in question_ids:
            question = line_item.find(f".//question[@question_id='{question_id}']")
            question_value = ''
            if question is not None:
                line_free_answer = question.find('line_free_answer')
                line_fixed_answer = question.find('line_fixed_answer')
                if line_free_answer is not None:
                    question_value = line_free_answer.text
                elif line_fixed_answer is not None:
                    question_value = line_fixed_answer.text
            question_description = question_data[question_id]
            question_item[question_description] = question_value

        question_values.append(question_item)

    for item in question_values:
        if "Selling Price-DO NOT ENTER '£' SIGN-DO NOT USE '.00'" in item:
            item["Selling Price"] = item.pop("Selling Price-DO NOT ENTER '£' SIGN-DO NOT USE '.00'")
        if "13 Digit Barcode" in item:
            item["Barcode"] = item.pop("13 Digit Barcode")
        if "Story Name - Menswear" in item:
            item["Story Name"] = item.pop("Story Name - Menswear")

    return question_values

data = parse_xml_file("XML.xml")
y = (data[0].get("Barcode"))

font_path = "font/Calibri/Calibri.ttf"
       
length = len(data)

all_img = []

for i in range(length):

    img = Image.open('layout.png')
    object = ImageDraw.Draw(img)

    value_1 = data[i].get("Primary Size")
    value_2 = data[i].get("Season Code")
    value_3 = data[i].get("Selling Price")
    value_4 = data[i].get("Barcode")
    value_5 = data[i].get("Story Name")

    print(value_1, value_2, value_3, value_4, value_5)

    if len(value_1) == 3:
        object.text((130,130), value_1 , font=ImageFont.truetype(font_path, 50), fill=(0,0,0))
    elif len(value_1) == 2:
        object.text((137,130), value_1 , font=ImageFont.truetype(font_path, 50), fill=(0,0,0))
    elif len(value_1) == 1:
        object.text((145,130), value_1 , font=ImageFont.truetype(font_path, 50), fill=(0,0,0))

    object.text((155,720), value_3 , font=ImageFont.truetype(font_path, 40), fill=(0,0,0))

    img = img.rotate(90, expand=True)
    object = ImageDraw.Draw(img)
    object.text((385,230), value_4 , font=ImageFont.truetype(font_path, 25), fill=(0,0,0))

    img = img.rotate(-90, expand=True)
    all_img.append(img)
    # img.save(f"image{i}.png")

num_images = len(all_img)
num_rows = (num_images + 5) // 6
num_cols = min(num_images, 6)

# Determine the size of each cell in the grid (assuming all images have the same size)
cell_width, cell_height = all_img[0].size

# Calculate the size of the final concatenated image
padding_between_images = 10  # Adjust this value to control the spacing between images
final_width = num_cols * cell_width + (num_cols - 1) * padding_between_images
final_height = num_rows * cell_height + (num_rows - 1) * padding_between_images

# Create a blank image to hold the concatenated images
concatenated_img = Image.new('RGB', (final_width, final_height), color=(255, 255, 255))

# Paste the individual images onto the blank image in the correct positions
for idx, img in enumerate(all_img):
    row = idx // 6
    col = idx % 6
    x_offset = col * (cell_width + padding_between_images)
    y_offset = row * (cell_height + padding_between_images)
    concatenated_img.paste(img, (x_offset, y_offset))

# Save or display the concatenated image
concatenated_img.save('concatenated_image1.png')
concatenated_img.save('concatenated_image1.pdf')
concatenated_img.show()