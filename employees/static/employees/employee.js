// employee_list.js
$(document).ready(function() {
    updateEmployeeList();
});

function updateEmployeeList() {
    console.log("In Js File")

    $.ajax({
        type: 'GET',
        url: '/api/employees/',
        dataType: 'json',
        success: function(data) {
            var employees = data.data;

            $('#employee-table-body').empty();

            for (var i = 0; i < employees.length; i++) {
                $('#employee-table-body').append('<tr>' +
                    '<td>' + employees[i].id + '</td>' +
                    '<td>' + employees[i].name + '</td>' +
                    '<td>' + employees[i].phone + '</td>' +
                    '<td>' + employees[i].email + '</td>' +
                    '<td>' + employees[i].department + '</td>' +
                    '<td>' +
                    '<a href="/employees/edit/' + employees[i].id + '"><button>Edit</button></a>' +
                    '<a href="/employees/delete/' + employees[i].id + '"><button>Delete</button></a>' +
                    '</td>' +
                    '</tr>');
            }
        },
        error: function(error) {
            console.error('Error fetching employee data:', error);
        }
    });
}

function openAddEmployeeForm() {
    // console.log("In Add Form")
    $.ajax({
        url: 'employees/add/',
        type: "GET",
        success: function (data) {
            $('#addEmployeeFormContainer').html(data);
            $('#addEmployeeModal').show();
        },
        error: function () {
            alert('Error loading Add Employee form.');
        }
    });
}   

function closeAddEmployeeForm() {
    $('#addEmployeeModal').hide();
}   

function submitForm() {
    console.log("In JS POST");
    var formData = {
        ename: document.getElementById('ename').value,
        ephone: document.getElementById('ephone').value,
        eemail: document.getElementById('eemail').value,
        edepartment: document.getElementById('edepartment').value
    };
    console.log(formData);
    $.ajax({
        type: "POST",
        url: '/api/employees/',
        contentType: "application/json",
        data: JSON.stringify(formData),
        success: function (response) {
            alert('Employee added successfully!');
            updateEmployeeList();
            closeModal();
        },
        error: function (xhr, status, error) {
            alert('Error adding employee. Please try again.');
            console.error('Error:', xhr.responseText);
        }
    });
}

function closeModal() {
    var modal = document.getElementById('addEmployeeModal');
    modal.style.display = 'none';
}


// function openEditEmployeeForm(employeeId) {
//     // Fetch employee details based on employeeId (you might use AJAX or other methods)
//     var employee = getEmployeeDetails(employeeId);

//     // Populate form fields with employee details
//     document.getElementById('ename').value = employee.name;
//     document.getElementById('ephone').value = employee.phone;
//     document.getElementById('eemail').value = employee.email;
//     document.getElementById('edepartment').value = employee.department;

//     // Display the edit form in a pop-up
//     var editModal = document.getElementById('editEmployeeModal');
//     editModal.style.display = 'block';
// }


function openEditEmployeeForm(employeeId) {
    console.log("Opening Edit Employee Form for ID:", employeeId);
    
    $.ajax({
        // url: '/api/employees/' + employeeId + '/',
        type: "GET",
        success: function (data) {
            var employee = data.data;

            // Log employee data
            console.log("Employee Data:", employee);

            // Populate the Edit Employee form with the employee data
            $('#editEmployeeForm #ename').val(employee.name);
            $('#editEmployeeForm #ephone').val(employee.phone);
            $('#editEmployeeForm #eemail').val(employee.email);
            $('#editEmployeeForm #edepartment').val(employee.department);

            // Display the modal
            $('#editEmployeeModal').show();
        },
        error: function (error) {
            console.error('Error loading Edit Employee form:', error);

            // Close the modal in case of an error
            $('#editEmployeeModal').hide();
        }
    });
}


function closeEditEmployeeForm() {
    $('#editEmployeeModal').hide();
}


