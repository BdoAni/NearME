'use strict'
// alert("you connected to js") 

const searchTools=document.querySelector('#search_tools')
if (searchTools){
    searchTools.addEventListener('submit', (evt) => {
        evt.preventDefault();
        // console.log(evt);
        const searched = document.querySelector('#search_tool_name').value;
        const url = `/search?searched=${searched.toLowerCase()}`;
        fetch(url)
            .then((response) => response.json())
            .then((responseJson) => {
                console.log(responseJson);
                const resultContainer = document.querySelector('#searched-result');
                // const content = element.innerHTML;
                for(let tool of responseJson){
                    // console.log(tool);
                    const resultRow = document.createElement("div");
                    const nameSpan = document.createElement('a')
                    nameSpan.setAttribute('href', `/tools/${tool.tool_id}`)
                    nameSpan.innerHTML=tool.tool_name;
                    const descriptionSpan = document.createElement('span')
                    descriptionSpan.innerHTML=tool.tool_description;
                    const priceSpan = document.createElement('span')
                    priceSpan.innerHTML=tool.tool_price;
                    resultRow.appendChild(nameSpan);
                    resultRow.appendChild(descriptionSpan);
                    resultRow.appendChild(priceSpan);
                    resultContainer.appendChild(resultRow);
                }
            })
            // .catch((err)=> console.log("Can't see the returned value!!"))
        });
}