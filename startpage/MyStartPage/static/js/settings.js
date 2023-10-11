function sprintf(text, ...args){
    let result = text;
    for (let arg of args){
        result = result.replace("%s", arg)
    }

    return result;
}

function replaceMultiple(text, replaceDictionary){
    let result = text;

    for(let key in replaceDictionary){
        let item = replaceDictionary[key];
        result = result.replaceAll(key, item);
    }

    return result;
}

function selectItem(item){
    let search_engine_dropdown = document.getElementById("search_engine_dropdown");
    search_engine_dropdown.innerHTML = item.innerHTML;
}

function getElementByPlaceholderText(item, placeholderText) {
  const elements = item.querySelectorAll("*");

  for (const element of elements) {
    if (element.placeholder === placeholderText) {
      return element;
    }
  }

  return null;
}

function removeSearchEngine(item){
    let nameLabel = getElementByPlaceholderText(item.parentNode, "Name");
    let name = nameLabel.value;
    let idName = name.replaceAll(" ", "-");

    let choiceElement = document.getElementById("search-engine-choice-${idName}".replaceAll("${idName}", idName));
    let search_engine_dropdown = document.getElementById("search_engine_dropdown");
    choiceElement.remove();
    item.parentNode.remove();

    if(search_engine_dropdown.innerHTML === choiceElement.innerHTML){
        try {
            search_engine_dropdown.innerHTML = document.getElementById("search_engines").querySelector(".form_row").querySelector('[id*="search-engine-name"]').value;
        }
        catch (e) {
            search_engine_dropdown.innerHTML = "";
        }
    }
}

function isValidId(str) {
  // Create a regular expression to match valid IDs.
  const regex = /^[a-zA-Z][a-zA-Z0-9_:\-]*$/;

  // Return true if the string matches the regular expression, false otherwise.
  return regex.test(str);
}

function addSearchEngine(item){
    let nameInput = document.getElementById("add_search_engine_name");
    let urlInput = document.getElementById("add_search_engine_url");

    let name = nameInput.value.trim();
    let url = urlInput.value.trim();

    if(!name || !url){
        return;
    }

    let idName = name.replaceAll(" ", "-");
    if(!isValidId(idName)){
        return;
    }
    nameInput.value = "";
    urlInput.value = "";

    let alreadyExistingItem = document.getElementById( sprintf("search-engine-url-%s", idName) )
    // Replace it if exists
    if(alreadyExistingItem !== null){
        alreadyExistingItem.value = url;
        return;
    }

    let search_engines_list = document.getElementById("search_engines");
    const templateStr =
        '<div class="form_row">' +
            '<label class="settings_label mx-2">Name</label>&nbsp;&nbsp;' +
            '<input type="text" class="form-control settings_input_box_small" placeholder="Name" value="${name}" id="search-engine-name-${idName}" readonly>' +
            '<label class="settings_label mx-2">Url</label>&nbsp;&nbsp;' +
            '<input type="text" class="form-control settings_input_box_big" placeholder="Url" value="${url}" id="search-engine-url-${idName}" readonly>&nbsp;&nbsp;&nbsp;&nbsp;' +
            '<button class="btn btn-danger settings_plusminus" onclick="removeSearchEngine(this);"><img src="../static/css/icons/ui/close.png" alt=""/></button>&nbsp;' +
            '<button class="btn btn-warning settings_plusminus" onclick="moveUp(this);"><img src="../static/css/icons/ui/up_arrow.png" alt=""/></button>&nbsp;' +
            '<button class="btn btn-warning settings_plusminus" onclick="moveDown(this);"><img src="../static/css/icons/ui/down_arrow.png" alt=""/></button>&nbsp;' +
        '</div>';

    search_engines_list.innerHTML += replaceMultiple(templateStr, {
        "${name}": name,
        "${url}": url,
        "${idName}": idName,
    });

    let search_engine_dropdown = document.getElementById("search-engine-dropdown");
    const templateChoiceStr =
        '<a class="dropdown-item" href="javascript:void(0);" data-value="${name}" onclick="selectItem(this);" id="search-engine-choice-${idName}">${name}</a>';
    search_engine_dropdown.innerHTML += replaceMultiple(templateChoiceStr, {
        "${name}": name,
        "${idName}": idName,
    });

    let dropdownItem = document.getElementById("search_engine_dropdown");
    if(dropdownItem.innerHTML === ""){
        dropdownItem.innerHTML = name;
    }
}

function removeParentGenerations(item, generationNumber){
    let i = 0;
    while(i < generationNumber){
        item = item.parentNode;
        i ++;
    }
    item.remove();
}

function removeCurrency(item){
    item.parentNode.remove();
}

function addCurrency(item){
    let addCurrencyBaseInput = document.getElementById("add-currency-base");
    let addCurrencyTargetInput = document.getElementById("add-currency-target");

    let baseStr = addCurrencyBaseInput.value.trim().toUpperCase();
    let targetStr = addCurrencyTargetInput.value.trim().toUpperCase();

    if(!baseStr || !targetStr){
        return;
    }

    addCurrencyBaseInput.value = "";
    addCurrencyTargetInput.value = "";

    let currencyList = document.getElementById("currency-list");
    const templateStr =
        '<div class="form_row">' +
            '<label class="settings_label mx-2">Base</label>&nbsp;&nbsp;' +
            '<input type="text" class="form-control settings_input_box_small currency_base_class" placeholder="Base Currency" value="${base}" readonly>' +
            '<label class="settings_label mx-2">Target</label>&nbsp;&nbsp;' +
            '<input type="text" class="form-control settings_input_box_small currency_target_class" placeholder="Target Currency" value="${target}" readonly>&nbsp;&nbsp;&nbsp;&nbsp;' +
            '<button class="btn btn-danger settings_plusminus" onclick="removeParentGenerations(this, 1);"><img src="../static/css/icons/ui/close.png" alt=""/></button>&nbsp;' +
            '<button class="btn btn-warning settings_plusminus" onclick="moveUp(this);"><img src="../static/css/icons/ui/up_arrow.png" alt=""/></button>&nbsp;' +
            '<button class="btn btn-warning settings_plusminus" onclick="moveDown(this);"><img src="../static/css/icons/ui/down_arrow.png" alt=""/></button>&nbsp;' +
        '</div>';

    currencyList.innerHTML += replaceMultiple(templateStr, {
        "${base}": baseStr,
        "${target}": targetStr
    });
}

function addWebsiteToCategory(item, category_name){
    let addWebsiteNameInput = document.getElementById(sprintf("%s-add-website-name", category_name));
    let addWebsiteUrlInput = document.getElementById(sprintf("%s-add-website-url", category_name));

    let name = addWebsiteNameInput.value.trim();
    let url = addWebsiteUrlInput.value.trim();

    if(!name || !url){
        return;
    }

    addWebsiteNameInput.value = "";
    addWebsiteUrlInput.value = "";

    let websiteListItem = document.getElementById(sprintf("%s-website-list", category_name));
    let templateStr =
        '<div class="form_row">' +
            '<label class="settings_label mx-2">Name</label>&nbsp;&nbsp;' +
            '<input type="text" class="form-control settings_input_box_small content_website_name" placeholder="Name" value="${name}" readonly>' +
            '<label class="settings_label mx-2">Url</label>&nbsp;&nbsp;' +
            '<input type="text" class="form-control settings_input_box_big content_website_url" placeholder="Url" value="${url}" readonly>&nbsp;&nbsp;&nbsp;&nbsp;' +
            '<button class="btn btn-danger settings_plusminus" onclick="removeParentGenerations(this, 1);"><img src="../static/css/icons/ui/close.png" alt=""/></button>&nbsp;' +
            '<button class="btn btn-warning settings_plusminus" onclick="moveUp(this);"><img src="../static/css/icons/ui/up_arrow.png" alt=""/></button>&nbsp;' +
            '<button class="btn btn-warning settings_plusminus" onclick="moveDown(this);"><img src="../static/css/icons/ui/down_arrow.png" alt=""/></button>&nbsp;' +
        '</div>';

    websiteListItem.innerHTML += replaceMultiple(templateStr, {
        "${name}": name,
        "${url}": url
    });
}

function addCategory(item) {
    let addCategoryName = document.getElementById("add-category-name");
    let name = addCategoryName.value;
    let idName = name.replaceAll(" ", "-");

    if(!name || !idName){
        return;
    }

    addCategoryName.value = "";

    let categoriesList = document.getElementById("categories_list");
    let templateStr =
        '<div class="category_row"><h2 class="settings_label settings_content_title category_title">${name}</h2><div id="${idName}-website-list"></div>' +
            '<h4 class="settings_label">Add a website to this category</h4>' +
            '<div class="form_row">' +
                '<label class="settings_label mx-2">Name</label>&nbsp;&nbsp;' +
                '<input type="text" class="form-control settings_input_box_small" placeholder="Name" id="${idName}-add-website-name">' +
                '<label class="settings_label mx-2">Url</label>&nbsp;&nbsp;' +
                '<input type="text" class="form-control settings_input_box_big" placeholder="Url" id="${idName}-add-website-url">&nbsp;&nbsp;&nbsp;&nbsp;' +
                '<button class="btn btn-primary settings_plusminus" onclick="addWebsiteToCategory(this, \'${idName}\');"><img src="../static/css/icons/ui/plus.png"/></button>' +
            '</div>' +
            '<button class="btn btn-danger" onclick="removeParentGenerations(this, 1);">Delete This Category</button>' +
            '<button class="btn btn-warning" onclick="moveCategoryUp(this);">Move This Category Up</button>' +
            '<button class="btn btn-warning" onclick="moveCategoryDown(this);">Move This Category Down</button>' +
            '<br><br><br>' +
        '</div>';

    let finalStr = replaceMultiple(templateStr, {
        "${name}": name,
        "${idName}": idName
    });
    categoriesList.innerHTML += finalStr;
}

function saveSettings() {
    let search_engines = {};
    let name = "";
    let lat = 0;
    let lng = 0;
    let currentSearchEngine = "";
    let currencyList = [];
    let categoriesList = [];

    let nameInput = document.getElementById("nameOption");
    let latitudeInput = document.getElementById("latitude");
    let longitudeInput = document.getElementById("longitude");

    let searchEnginesDiv = document.getElementById("search_engines");
    let searchEngineItems = searchEnginesDiv.querySelectorAll(".form_row");
    searchEngineItems.forEach(item => {
        let search_engine_name = item.querySelector('[id*="search-engine-name"]').value;
        let search_engine_url = item.querySelector('[id*="search-engine-url"]').value;

        search_engines[search_engine_name] = search_engine_url;
    });

    let currenciesDiv = document.getElementById("currency-list");
    let currenciesItems = currenciesDiv.querySelectorAll('.form_row');
    currenciesItems.forEach(item => {
        let baseStr = item.querySelector(".currency_base_class").value;
        let targetStr = item.querySelector(".currency_target_class").value;

        let currencyDict = {};
        currencyDict[baseStr] = targetStr;
        currencyList.push(currencyDict);
    });

    let categoriesDiv = document.getElementById("categories_list");
    let categoryItems = categoriesDiv.querySelectorAll('.category_row');
    categoryItems.forEach(item => {
        let name = item.querySelector('.category_title').innerHTML;
        let websiteDivs = item.querySelector('[id*="website-list"]').querySelectorAll('.form_row');
        let website_list = [];
        websiteDivs.forEach(subitem => {
            let name = subitem.querySelector(".content_website_name").value;
            let url = subitem.querySelector(".content_website_url").value;
            let websiteData = {};
            websiteData["name"] = name;
            websiteData["url"] = url;
            website_list.push(websiteData);
        });

        let currentContent = {};
        currentContent["name"] = name;
        currentContent["content"] = website_list;
        categoriesList.push(currentContent);
    });

    name = nameInput.value;
    lat = latitudeInput.value;
    lng = longitudeInput.value;
    currentSearchEngine = document.getElementById("search_engine_dropdown").innerHTML;

    let finalJSON = {
        "name": name,
        "latitude": lat,
        "longitude": lng,
        "search_engines": search_engines,
        "current_search_engine": currentSearchEngine,
        "currencies": currencyList,
        "categories": categoriesList,
    };

    let requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(finalJSON)
    };

    fetch('/save_settings/', requestOptions)
        .then(function (response) {
            if (response.ok){
                location.reload();
            }
        });
}

function resetSettings() {
    if(window.confirm("Are you sure to reset your settings to default?")){
        fetch("/reset_settings/")
        .then(function () {
            location.reload();
        });
    }
}

function returnToStartPage() {
    window.location.href = "/";
}

function swap(node1, node2) {
    const afterNode2 = node2.nextElementSibling;
    const parent = node2.parentNode;
    node1.replaceWith(node2);
    parent.insertBefore(node1, afterNode2);
}

function moveUp(item) {
    let parent = item.parentNode.parentNode;
    let rows = parent.querySelectorAll('.form_row')
    for(let i = 1; i < rows.length; ++i){
        let currentNode = rows[i];
        if(currentNode.isEqualNode(item.parentNode)){
            let previousNode = rows[i - 1];
            currentNode.parentNode.insertBefore(currentNode, previousNode);
            break;
        }
    }
}

function moveDown(item) {
    let parent = item.parentNode.parentNode;
    let rows = parent.querySelectorAll('.form_row')
    for(let i = 0; i < rows.length - 1; ++i){
        let currentNode = rows[i];
        if(currentNode.isEqualNode(item.parentNode)){
            let nextNode = rows[i + 1];
            nextNode.parentNode.insertBefore(nextNode, currentNode);
            break;
        }
    }
}

function moveCategoryUp(item){
    let parent = item.parentNode.parentNode;
    let rows = parent.querySelectorAll('.category_row')
    for(let i = 1; i < rows.length; ++i){
        let currentNode = rows[i];
        if(currentNode.isEqualNode(item.parentNode)){
            let previousNode = rows[i - 1];
            currentNode.parentNode.insertBefore(currentNode, previousNode);
            break;
        }
    }
}

function moveCategoryDown(item) {
    let parent = item.parentNode.parentNode;
    let rows = parent.querySelectorAll('.category_row')
    for(let i = 0; i < rows.length - 1; ++i){
        let currentNode = rows[i];
        if(currentNode.isEqualNode(item.parentNode)){
            let nextNode = rows[i + 1];
            nextNode.parentNode.insertBefore(nextNode, currentNode);
            break;
        }
    }
}