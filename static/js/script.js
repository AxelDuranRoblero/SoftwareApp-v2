const form = document.getElementById('loginForm');
const alertBox = document.getElementById('alert');

function showAlert(message, type) {
    alertBox.textContent = message;
    alertBox.className = `alert alert-${type} show`;
    
    setTimeout(() => {
        alertBox.classList.remove('show');
    }, 5000);
}

function calculateAge(birthDate) {
    const today = new Date();
    const birth = new Date(birthDate);
    let age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
        age--;
    }
    
    return age;
}

form.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const nombre = document.getElementById('nombre').value;
    const email = document.getElementById('email').value;
    const pais = document.querySelector('input[name="pais"]:checked');
    const identificador = document.getElementById('identificador').value;
    const fechaNacimiento = document.getElementById('fecha_nacimiento').value;
    
    
    if (!pais) {
        showAlert('Por favor seleccione su país', 'error');
        return;
    }
    
    const edad = calculateAge(fechaNacimiento);
    if (edad < 18) {
        showAlert('Debe ser mayor de 18 años para acceder', 'error');
        
        return;
    }
    
   
    showAlert(`¡Bienvenido ${nombre}!
Datos recibidos correctamente`, 'success');
    

    console.log({
        nombre,
        email,
        pais: pais.value,
        identificador,
        fechaNacimiento,
        edad
    });
 
});


document.querySelectorAll('input').forEach(input => {
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && input.type !== 'submit') {
            e.preventDefault();
        }
     
    });
});