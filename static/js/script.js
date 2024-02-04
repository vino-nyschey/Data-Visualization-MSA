
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

function sortTable(col) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("protein-table");
    switching = true;
    dir = "asc";
    /* Make a loop that will continue until
    no switching has been done: */
    while (switching) {
        // Start by saying: no switching is done:
        switching = false;
        rows = table.rows;
        /* Loop through all table rows (except the
        first, which contains table headers): */
        for (i = 1; i < (rows.length - 1); i++) {
            // Start by saying there should be no switching:
            shouldSwitch = false;
            /* Get the two elements you want to compare,
            one from current row and one from the next: */
            x = rows[i].getElementsByTagName("TD")[col];
            y = rows[i + 1].getElementsByTagName("TD")[col];
            /* Check if the two rows should switch place,
            based on the direction, asc or desc: */
            if (dir == "asc") {
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    // If so, mark as a switch and break the loop:
                    shouldSwitch= true;
                    break;
                }
            } else if (dir == "desc") {
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                    // If so, mark as a switch and break the loop:
                    shouldSwitch= true;
                    break;
                }
            }
        }
        if (shouldSwitch) {
            /* If a switch has been marked, make the switch
            and mark that a switch has been done: */
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            // Each time a switch is done, increase switchcount by 1:
            switchcount ++;
        } else {
            /* If no switching has been done AND the direction is "asc",
            set the direction to "desc" and run the while loop again. */
            if (switchcount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
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