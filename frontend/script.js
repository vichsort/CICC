document.addEventListener('DOMContentLoaded', () => {
    const vehicleSelect = document.getElementById('vehicle');
    const vehicleTypeContainer = document.getElementById('vehicleTypeContainer');
    const vehicleTypeSelect = document.getElementById('vehicle_type');
    const fuelContainer = document.getElementById('fuelContainer');
    const fuelSelect = document.getElementById('fuel');
    const peopleAmountContainer = document.getElementById('peopleAmountContainer');
    const peopleAmountInput = document.getElementById('people_amount');

    // Mapeamento dos limites de pessoas por tipo de veículo
    const peopleLimits = {
        car: 5,
        motorcycle: 2
    };
    
    // Mapeamento de tipos de veículos e combustíveis
    const vehicleTypes = {
        car: ["Standard", "Flex"],
        motorcycle: ["Standard", "Flex"],
        bus: ["Micro-Bus", "Municipal Bus", "Travel Bus"]
    };

    const fuelOptions = {
        car_standard: ["Gasolina"],
        car_flex: ["Gasolina", "Etanol"],
        motorcycle_standard: ["Gasolina"],
        motorcycle_flex: ["Gasolina", "Etanol"],
        'bus_micro-bus': ["Diesel"],
        'bus_municipal-bus': ["Diesel", "Biodiesel"],
        'bus_travel-bus': ["Diesel", "Biodiesel"]
    };

    function populateSelect(selectElement, options, selectFirst = false) {
        selectElement.innerHTML = '<option value="" disabled selected>Selecione uma opção</option>';
        if (options && options.length > 0) {
            options.forEach(option => {
                const el = document.createElement('option');
                el.value = option.toLowerCase().replace(/ /g, '-');
                el.textContent = option;
                selectElement.appendChild(el);
            });
            // Adiciona a lógica para selecionar o primeiro item
            if (selectFirst) {
                selectElement.selectedIndex = 1;
            }
        }
    }

    vehicleSelect.addEventListener('change', (event) => {
        const selectedVehicle = event.target.value;

        // Reset and hide/show sections
        vehicleTypeContainer.style.display = 'none';
        peopleAmountContainer.style.display = 'none';
        fuelContainer.style.display = 'none';
        peopleAmountInput.required = false;

        // Show Vehicle Type
        if (selectedVehicle === 'car' || selectedVehicle === 'motorcycle' || selectedVehicle === 'bus') {
            vehicleTypeContainer.style.display = 'block';
            populateSelect(vehicleTypeSelect, vehicleTypes[selectedVehicle], true); // Seleciona o 1º item

            // Only show people amount for car and motorcycle
            if (selectedVehicle === 'car' || selectedVehicle === 'motorcycle') {
                peopleAmountContainer.style.display = 'block';
                peopleAmountInput.required = true;
                // Seta o limite máximo de pessoas
                peopleAmountInput.max = peopleLimits[selectedVehicle];
            }
        }
    });

    vehicleTypeSelect.addEventListener('change', (event) => {
        const selectedVehicle = vehicleSelect.value;
        const selectedType = event.target.value;
        
        // Hide fuel container for Standard vehicles and Micro-Bus
        if ((selectedVehicle !== 'bus' && selectedType === 'standard') || selectedType === 'micro-bus') {
            fuelContainer.style.display = 'none';
            fuelSelect.removeAttribute('required');
        } else {
            fuelContainer.style.display = 'block';
            fuelSelect.setAttribute('required', 'required');
            const fuelKey = `${selectedVehicle}_${selectedType}`;
            const fuels = fuelOptions[fuelKey];
            populateSelect(fuelSelect, fuels, true); // Seleciona o 1º item
        }
    });

    const form = document.getElementById('vehicleForm');
    form.addEventListener('submit', (event) => {
        event.preventDefault();

        const selectedVehicle = document.getElementById('vehicle').value;
        const selectedType = document.getElementById('vehicle_type').value;

        // Validação do limite de pessoas
        if (selectedVehicle in peopleLimits) {
            const people = parseInt(peopleAmountInput.value, 10);
            if (people > peopleLimits[selectedVehicle]) {
                alert(`Número de pessoas para ${selectedVehicle} não pode ser maior que ${peopleLimits[selectedVehicle]}.`);
                return; // Impede o envio do formulário
            }
        }

        // Prepara os dados para envio
        const data = {
            person_name: document.getElementById('person_name').value,
            distance: parseFloat(document.getElementById('distance').value.replace(',', '.')).toFixed(2), // Adiciona . na km
            vehicle: selectedVehicle
        };
        
        if (peopleAmountContainer.style.display !== 'none') {
            data.people_amount = peopleAmountInput.value;
        }

        data.vehicle_type = selectedType;
        if (selectedVehicle !== 'bus' && selectedType === 'standard') {
            data.fuel = 'Gasolina';
        } else if (selectedType === 'micro-bus') {
            data.fuel = 'Diesel';
        } else {
            data.fuel = fuelSelect.value;
        }

        console.log(data);
        alert('Formulário enviado com sucesso! Verifique o console para os dados.');
    });
});