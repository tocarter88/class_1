const generate_story_button = document.getElementById("generateStory")


generate_story_button.addEventListener('click', handleGenerateStory)

// Extracts the data URL from img elements and descriptions from textarea elements
// within image_card class elements, then calls the backend /generate_story endpoint
// with the collected image data and descriptions, and displays the returned story
async function handleGenerateStory() {
    image_cards = document.getElementsByClassName("image_card")
    image_urls_with_desc = []
    for (i = 0; i < image_cards.length; i++) {
        image_card = image_cards[i]
        img_elems = image_card.getElementsByTagName("img")
        if (img_elems.length == 0) {
            continue
        }
        img_elem = img_elems[0]
        data_url = img_elem.src

        textarea_elems = image_card.getElementsByTagName("textarea")
        if (textarea_elems.length == 0) {
            continue
        }
        textarea_elem = textarea_elems[0]
        description = textarea_elem.value

        image_urls_with_desc.push({
                "data_url": data_url,
                "description": description,
            }
        )        
    }

    response = await fetch("/generate_story", 
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(image_urls_with_desc)
        }
    )

    response_obj = await response.json()

    document.getElementById("storyTextArea").innerHTML = response_obj["story"]
}