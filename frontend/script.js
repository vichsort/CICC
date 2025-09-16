document.addEventListener('DOMContentLoaded', () => {
    const vehicleSelect = document.getElementById('vehicle');
    const vehicleTypeContainer = document.getElementById('vehicleTypeContainer');
    const vehicleTypeSelect = document.getElementById('vehicle_type');
    const fuelContainer = document.getElementById('fuelContainer');
    const fuelSelect = document.getElementById('fuel');
    const peopleAmountContainer = document.getElementById('peopleAmountContainer');

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

    function populateSelect(selectElement, options) {
        selectElement.innerHTML = '<option value="" disabled selected>Selecione uma opção</option>';
        if (options) {
            options.forEach(option => {
                const el = document.createElement('option');
                el.value = option.toLowerCase().replace(/ /g, '-');
                el.textContent = option;
                selectElement.appendChild(el);
            });
        }
    }

    vehicleSelect.addEventListener('change', (event) => {
        const selectedVehicle = event.target.value;

        // Reset and hide/show sections
        vehicleTypeContainer.style.display = 'none';
        peopleAmountContainer.style.display = 'none';
        fuelContainer.style.display = 'none';
        document.getElementById('people_amount').required = false;

        // Show Vehicle Type and People Amount for Cars and Motorcycles
        if (selectedVehicle === 'car' || selectedVehicle === 'motorcycle' || selectedVehicle === 'bus') {
            vehicleTypeContainer.style.display = 'block';
            populateSelect(vehicleTypeSelect, vehicleTypes[selectedVehicle]);
            
            // Only show people amount for car and motorcycle
            if (selectedVehicle === 'car' || selectedVehicle === 'motorcycle') {
                peopleAmountContainer.style.display = 'block';
                document.getElementById('people_amount').required = true;
            }
        }
    });

    vehicleTypeSelect.addEventListener('change', (event) => {
        const selectedVehicle = vehicleSelect.value;
        const selectedType = event.target.value;
        
        // Hide fuel container for Standard vehicles and Micro-Bus, as fuel is fixed
        if ((selectedVehicle !== 'bus' && selectedType === 'standard') || selectedType === 'micro-bus') {
            fuelContainer.style.display = 'none';
            fuelSelect.removeAttribute('required');
        } else {
            fuelContainer.style.display = 'block';
            fuelSelect.setAttribute('required', 'required');
            const fuelKey = `${selectedVehicle}_${selectedType}`;
            const fuels = fuelOptions[fuelKey];
            populateSelect(fuelSelect, fuels);
        }
    });

    const form = document.getElementById('vehicleForm');
    form.addEventListener('submit', (event) => {
        event.preventDefault();

        const selectedVehicle = document.getElementById('vehicle').value;
        const selectedType = document.getElementById('vehicle_type').value;

        const data = {
            person_name: document.getElementById('person_name').value,
            distance: document.getElementById('distance').value,
            vehicle: selectedVehicle
        };
        
        // Add optional fields only if they are visible
        if (peopleAmountContainer.style.display !== 'none') {
            data.people_amount = document.getElementById('people_amount').value;
        }

        // Handle vehicle type and fuel logic
        data.vehicle_type = selectedType;
        if (selectedVehicle !== 'bus' && selectedType === 'standard') {
            data.fuel = 'Gasolina';
        } else if (selectedType === 'micro-bus') {
            data.fuel = 'diesel';
        } else {
            data.fuel = document.getElementById('fuel').value;
        }

        console.log(data);
        alert('Form submitted successfully! Check the console for the data.');
    });
});