

function openBuyForm() {
    document.getElementById("buyForm").style.display = "block";
    document.getElementById("overlay").classList.add("show");  // Dodaj klasę 'show'
    document.body.style.overflow = 'hidden'; // Zablokuj przewijanie strony
}

function closeBuyForm() {
    document.getElementById("buyForm").style.display = "none";
    document.getElementById("overlay").classList.remove("show");  // Usuń klasę 'show'
    document.body.style.overflow = 'auto'; // Odblokuj przewijanie strony
}


function openSellForm() {
    document.getElementById("sellForm").style.display = "block";
    document.getElementById("overlay").classList.add("show");  // Dodaj klasę 'show'
    document.body.style.overflow = 'hidden'; // Zablokuj przewijanie strony
}

function closeSellForm() {
    document.getElementById("sellForm").style.display = "none";
    document.getElementById("overlay").classList.remove("show");  // Usuń klasę 'show'
    document.body.style.overflow = 'auto'; // Odblokuj przewijanie strony
}

function updateTickers() {
    console.log("updateTickers");
    var assetClassSelect = document.getElementById("asset_class_sell");
    console.log(used_asset_classes_dict);
    var tickerSelect = document.getElementById("ticker");
    var selectedAssetClass = assetClassSelect.value;
    var tickers = [];

    // Pobierz listę tickers dla wybranej klasy aktywów
    if (selectedAssetClass in used_asset_classes_dict) {
        tickers = used_asset_classes_dict[selectedAssetClass];
    }

    // Wyczyść istniejące opcje
    tickerSelect.innerHTML = "";

    // Dodaj nowe opcje
    for (var i = 0; i < tickers.length; i++) {
        var option = document.createElement("option");
        option.text = tickers[i];
        option.value = tickers[i];
        tickerSelect.add(option);
    }

    // Zaktualizuj wygląd selecta
    $('.select2').select2();
}

// Part used to update the Ticker select options based on the selected Asset Class in sell form
window.addEventListener('DOMContentLoaded', (event) => {
    const assetClassSelect = document.getElementById('asset_class_sell');
    const tickerSelect = document.getElementById('ticker');

    // Funkcja do aktualizacji opcji Tickerów na podstawie wybranej klasy aktywów
    function updateTickers() {
        const selectedAssetClass = assetClassSelect.value;
        tickerSelect.innerHTML = ''; // Wyczyść opcje Tickerów

        // Dodaj opcje Tickerów odpowiadające wybranej klasie aktywów
        window.usedAssetClassesDict[selectedAssetClass].forEach(ticker => {
            const option = document.createElement('option');
            option.value = ticker;
            option.textContent = ticker;
            tickerSelect.appendChild(option);
        });
    }

    // Wywołaj funkcję aktualizacji przy zmianie wybranej klasy aktywów
    assetClassSelect.addEventListener('change', updateTickers);

    // Wywołaj funkcję aktualizacji na starcie, aby ustawić opcje Tickerów zgodnie z domyślną klasą aktywów
    updateTickers();
});