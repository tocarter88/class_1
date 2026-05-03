const imageUpload = document.getElementById('imageUpload');
const previewContainer = document.getElementById('previewContainer');
const storyContainer = document.getElementById("storyContainer");

// Listen for file selection
imageUpload.addEventListener('change', handleFileSelect);

// Handles file selection event from the imageUpload input element
// Extracts selected files and passes them to processImageFile for processing
function handleFileSelect(event) {
    const files = event.target.files; // Get selected files
    if (!files.length) return; // Exit if no files selected

    processImageFile(files);
}

// Adapter to FileReader.
// So that the caller can use await to get the data URL instead of using onload 
// callback.
function readFileAsync(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
    
        reader.onload = function(e){
            resolve(e.target.result); // Data URL 
        };
    
        reader.onerror = () => reject(reader.error);
    
        reader.readAsDataURL(file); 
    });
}

// Processes image files by reading them as data URLs, creating image_card div elements
// with img previews, calling the /summary_image backend endpoint to generate descriptions,
// and displaying editable textarea fields with the descriptions
async function processImageFile(files) {

    data_urls = [];
    image_cards = [];
    fetching_elems = [];
    previewContainer.innerHTML = ""

    // Read the file as a data URL
    for (var file of files){
        data_url = await readFileAsync(file)
        data_urls.push(data_url)

        image_card = document.createElement("div")
        image_card.className = "image_card"

        img_elem = document.createElement("img")

        img_elem.src = data_url
        img_elem.className = "preview_img"
        image_card.appendChild(img_elem)

        fetching_elem = document.createElement("p")
        fetching_elem.innerHTML = "Fetching Description ... "
        image_card.appendChild(fetching_elem)
    
        fetching_elems.push(fetching_elem)
        image_cards.push(image_card)
        previewContainer.appendChild(image_card)
    }

    for (var i = 0; i < data_urls.length; i++) {
        response = await fetch("/summary_image", 
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({"url": data_urls[i]})
            }
        )
        
        response_json = await response.json()

        description_text_box = document.createElement("textarea")
        description_text_box.cols = 60
        description_text_box.value = response_json["description"]
        fetching_elems[i].remove()
        image_cards[i].appendChild(description_text_box)
    }

    storyContainer.classList.remove("hidden")
}

