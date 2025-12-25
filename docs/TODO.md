# TODO: Update Booking Data and Currency Conversion

## Tasks
- [x] Add destination field to Booking model for consistency (already exists)
- [x] Convert prices from VND to USD in ticket.html template
- [x] Convert prices from VND to USD in booking views and models
- [x] Update "Book Now" buttons in destination-details.html to redirect to booking with destination data
- [x] Update destination_detail view to pass destination data
- [x] Test the changes

## Notes
- Assuming 1 USD = 23,000 VND conversion rate
- All price displays now show USD
- Book Now buttons pass destination information to booking page
- Template paths reorganized - each module now has its own template directory
- Fixed core/views.py syntax errors and missing convert_vnd_to_usd function

## Completed Changes
1. Fixed syntax errors in core/views.py
2. Added convert_vnd_to_usd function to bookings/services.py
3. Updated ticket creation to use USD conversion (total_cost_usd)
4. All "Book Now" buttons in destination-details.html now include destination parameter
5. Updated CTA buttons to link to actual pages
6. Server running successfully at http://127.0.0.1:8000/