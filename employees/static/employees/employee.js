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


function openEditEmployeeForm(employeeId) {
    console.log(employeeId)
    $.ajax({
        url: `/employees/edit/${employeeId}/`,
        type: "GET",
        success: function (data) {
            $('#editEmployeeModal .modal-content').html(data);
            $('#editEmployeeModal').show();
        },
        error: function () {
            alert('Error loading Edit Employee form.');
        }
    });
    // Prevent default behavior (navigation)
    return false;
}

function closeEditEmployeeForm() {
    $('#editEmployeeModal').hide();
}