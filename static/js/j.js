jQuery.noConflict()
console.log("load!")
jQuery('#PickupModal').on('show.bs.modal', function () {
		if ($.fn.DataTable.isDataTable('#dynamicTable')) {
	table.destroy();
		}
table = $('#dynamicTable').DataTable({
	data: packages,
columns: [
{data: 'description' },
{data: 'dropoff_location' },
{data: 'demanding_user_id' },
{data: null, defaultContent: "" }
],
select: {
	style: 'multi',
			},
columnDefs: [{
	orderable: false,
className: 'select-checkbox',
targets: 3
			}]
		});
	});
jQuery('#btnSave').on('click', function () {
		var data = table.rows({selected: true }).data();
console.log(data);

	});
jQuery('.btnModalDismiss').on('click', function () {
	jQuery('#PickupModal').modal('hide');
	});
jQuery('.marker').on('click', function () {
	current_id = jQuery(this).attr('id');
packages = getPerLocation(current_id);
jQuery(
'#PickupModal'
).modal('show');
	});
jQuery('body div.container').removeClass('container').
addClass('container-fluid').addClass('p-0').addClass('m-0');
jQuery("#RangeSlider").on("input", function () {

	setInterval(function () {
		let range = jQuery("#RangeSlider").val();
		if (prev_range != range) {
			prev_range = range;
			//*call server
			map.getSource('polygon').setData(createGeoJSONCircle(coordsTuple, prev_range).data);
		}
	}, 1000);
	});

