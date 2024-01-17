// employee_list.js
$(document).ready(function() {
    updateEmployeeList();

    $('#editEmployeeForm').submit(function (event) {
        event.preventDefault();  // Prevent the default form submission
        submitEditForm();
    });
});

function updateEmployeeList() {
    console.log("In Js File")

    $.ajax({
        type: 'GET',
        url: '/api/employees/',
        dataType: 'json',
        success: function(data) {
            var employees = data.data;
            // console.log("employee=",data)
            $('#employee-table-body').empty();

            for (var i = 0; i < employees.length; i++) {
                $('#employee-table-body').append('<tr>' +
                    '<td>' + employees[i].id + '</td>' +
                    '<td>' + employees[i].name + '</td>' +
                    '<td>' + employees[i].phone + '</td>' +
                    '<td>' + employees[i].email + '</td>' +
                    '<td>' + employees[i].department + '</td>' +
                    '<td>' +
                    // '<button data-employee-id="' + employees[i].id + '" onclick="openEditEmployeeForm(' + employees[i].id + ')">Edit</button>' +
                    '<button data-employee-id=' + employees[i].id + ' onclick="openEditEmployeeForm(this)">Edit</button>' +
                    '<a><button>Delete</button></a>' +
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
    // console.log("In JS POST");
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

            // Clear form fields after successful submission
            $('#employeeForm :input').val('');
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

var employeeId;

function openEditEmployeeForm(clickedButton) {
    // Retrieve the employee ID from the data attribute
    var employeeId = $(clickedButton).data('employee-id');
    // console.log(employeeId);
    $.ajax({
        url: '/employees/edit/' + employeeId + '/',
        type: "GET",
        success: function (data) {
            // console.log(data.employee.id)
            // Set the values in the form fields
            $('#edit-employee-id').val(data.employee.id);
            $('#edit-ename').val(data.employee.name);
            $('#edit-ephone').val(data.employee.phone);
            $('#edit-eemail').val(data.employee.email);
            $('#edit-edepartment').val(data.employee.department);
            $('#editEmployeeModal').show()
        },
        error: function () {
            alert('Error loading Edit Employee form.');
        }
    });
}

function closeEditEmployeeForm() {
    $('#editEmployeeModal').hide();
}


function submitEditForm() {
    // Retrieve form data
    var formData = {
        employeeId: $('#edit-employee-id').val(),
        ename: $('#edit-ename').val(),
        ephone: $('#edit-ephone').val(),
        eemail: $('#edit-eemail').val(),
        edepartment: $('#edit-edepartment').val()        
    };
    console.log(formData);
    console.log(formData.employeeId);

    // Make AJAX request to update employee data
    $.ajax({
        type: "PUT",
        url: '/api/employees/' + formData.employeeId + '/',
        contentType: "application/json",
        data: JSON.stringify(formData),
        success: function (response) {
            alert('Employee updated successfully!');
            updateEmployeeList();
            closeEditEmployeeForm();
        },
        error: function (xhr, status, error) {
            console.error('Error:', xhr.responseText);
            alert('Error updating employee. Please try again.');
        }
    });
}