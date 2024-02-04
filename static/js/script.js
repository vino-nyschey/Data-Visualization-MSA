
$(document).ready(function () {
    // add click event for detail buttons
    $('#protein-table tbody').on('click', '.protein-info-btn', function () {
        // find out the sequence, which detailed button was clicked
        var sequence_id = $(this).closest('tr').data('sequence-id');

        // loead protein details for clicked details button
        loadProteinDetails(sequence_id);
        scrollToDetails();
    });

    // function to scroll down
    function scrollToDetails() {
        $('html, body').animate({
            scrollTop: $('#protein-details').offset().top
        }, 900);
    }

    // function to loead protein details
    function loadProteinDetails(sequence_id) {
        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: '/get_protein_details',
            data: JSON.stringify({'sequence_id': sequence_id}),
            success: function (data) {
                if (data) {
                    var details = '<table class="protein-detail-table">' +
                                    '<tr><td><strong>PDB ID:</strong></td><td>' + data['PDB ID'] + '</td></tr>' +
                                    '<tr><td><strong>Organism:</strong></td><td>' + data['Organism'] + '</td></tr>' +
                                    '<tr><td><strong>Protein Name:</strong></td><td>' + data['Protein Name'] + '</td></tr>' +
                                    '<tr><td><strong>Protein Family:</strong></td><td>' + data['Protein Family'] + '</td></tr>' +
                                    '<tr><td><strong>Discovered Year:</strong></td><td>' + (data['Discovered Year'] || 'N/A') + '</td></tr>' +
                                    '<tr><td><strong>Number of Chains:</strong></td><td>' + (data['No. of Chains'] || 'N/A') + '</td></tr>' +
                                    '<tr><td><strong>Engineered:</strong></td><td>' + (data['Engineered'] || 'N/A') + '</td></tr>' +
                                    '<tr><td><strong>Sequence Length:</strong></td><td>' + (data['Sequence Length'] || 'N/A') + '</td></tr>' +
                                    '</table>';
                                $('#protein-details').html(details);
                    
                    // Display sequence with color-coded amino acids
                    var sequence = data['Sequence'] || 'N/A';
                    var formattedSequence = '';
                    for (var i = 0; i < sequence.length; i++) {
                        formattedSequence += '<span class="amino-acid" style="color: ' + getAminoAcidColor(sequence[i]) + ';">' + sequence[i] + '</span>';
                        if ((i + 1) % 60 === 0) {
                            formattedSequence += '<br>';
                        }
                    }
                    $('#sequence-details').html(formattedSequence);
                } else {
                    $('#protein-details').html('<p>No details found for this protein.</p>');
                    $('#sequence-details').html('');
                }
            },
            error: function () {
                $('#protein-details').html('<p>Error fetching protein details.</p>');
                $('#sequence-details').html('');
            }
        });
    }

    // show details of the first protein weithout clicking button details
    loadProteinDetailsForFirstItem();

    // function to load protein details for the first protein
    function loadProteinDetailsForFirstItem() {
        var firstRow = $('#protein-table tbody tr:first');
        if (firstRow.length > 0) {
            var sequence_id = firstRow.data('sequence-id');
            loadProteinDetails(sequence_id);
        }
    }
});

// Initialize sorting direction array
var sortDirections = [];
    
function sortTable(columnIndex) {
    var table, rows, switching, i, x, y, shouldSwitch;
    table = document.getElementById("protein-table");
    switching = true;

    // Initialize sorting direction for the column if not set
    if (!sortDirections[columnIndex]) {
        sortDirections[columnIndex] = "asc";
    }

    while (switching) {
        switching = false;
        rows = table.getElementsByTagName("tr");
        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("td")[columnIndex];
            y = rows[i + 1].getElementsByTagName("td")[columnIndex];

            // Convert to numbers for comparison if possible
            var xValue = parseFloat(x.innerHTML.replace(/[^0-9.-]+/g,""));
            var yValue = parseFloat(y.innerHTML.replace(/[^0-9.-]+/g,""));

            if (!isNaN(xValue) && !isNaN(yValue)) {
                if (sortDirections[columnIndex] == "asc") {
                    if (xValue > yValue) {
                        shouldSwitch= true;
                        break;
                    }
                } else if (sortDirections[columnIndex] == "desc") {
                    if (xValue < yValue) {
                        shouldSwitch= true;
                        break;
                    }
                }
            } else {
                // If not numeric, compare as strings
                if (sortDirections[columnIndex] == "asc") {
                    if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                        shouldSwitch= true;
                        break;
                    }
                } else if (sortDirections[columnIndex] == "desc") {
                    if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                        shouldSwitch= true;
                        break;
                    }
                }
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
        }
    }

    // Toggle sorting direction
    if (sortDirections[columnIndex] === "asc") {
        sortDirections[columnIndex] = "desc";
    } else {
        sortDirections[columnIndex] = "asc";
    }
}

// function to get Clustal color coding for amino acids
function getAminoAcidColor(aminoAcid) {
    switch (aminoAcid.toUpperCase()) {
        case 'G':
        case 'P':
        case 'S':
        case 'T':
            return 'orange';
        case 'H':
        case 'K':
        case 'R':
            return 'red';
        case 'F':
        case 'W':
        case 'Y':
            return 'blue';
        case 'I':
        case 'L':
        case 'M':
        case 'V':
            return 'green';
        case 'D':
        case 'E':
            return 'purple';
        default:
            return 'black';
    }
}