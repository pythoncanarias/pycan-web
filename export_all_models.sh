#!/bin/bash

# Speakers
./manage.py export_model speakers Social
./manage.py export_model speakers Speaker
./manage.py export_model speakers Contact

# Notice
./manage.py export_model notices NoticeKind
./manage.py export_model notices Notice

# About

./manage.py export_model about Ally
./manage.py export_model about FAQItem

# Events

./manage.py export_model events Event
./manage.py export_model events Badge
./manage.py export_model events Proposal
./manage.py export_model events WaitingList
./manage.py export_model events Refund

# Locations

./manage.py export_model locations Venue
./manage.py export_model locations Location

# Tickets

./manage.py export_model tickets Article
./manage.py export_model tickets TicketCategory
./manage.py export_model tickets Ticket
./manage.py export_model tickets Raffle
./manage.py export_model tickets Gift

# Schedule

./manage.py export_model schedule Schedule
./manage.py export_model schedule Track
./manage.py export_model schedule Slot
./manage.py export_model schedule SlotLevel
./manage.py export_model schedule SlotTag
./manage.py export_model schedule SlotCategory

# Members

./manage.py export_model members Member
./manage.py export_model members Position
./manage.py export_model members Membership

# Invoices

./manage.py export_model invoices Client
./manage.py export_model invoices Concept
./manage.py export_model invoices Invoice

# Quotes

./manage.py export_model quotes Author
./manage.py export_model quotes Quote

# Learn

./manage.py export_model learn Label
./manage.py export_model learn Resource

# Jobs

./manage.py export_model jobs JobOffer

# Organizations

./manage.py export_model organizations Organization
./manage.py export_model organizations OrganizationRole
./manage.py export_model organizations OrganizationCategory
./manage.py export_model organizations Membership

zip exported.zip exported/*.json
