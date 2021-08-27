import math

from ticket.models import Ticket
from config.ticket import TICKET_STATUS, TICKET_PAGE_COUNT, TICKET_USERS, TICKET_ACTION


class TicketValidation:
    def check_ticket_user(self, user_type):
        return True if user_type in TICKET_USERS else False

    def is_ticket_action_valid(self, action):
        return True if action in TICKET_ACTION else False

    def make_ticket(self, user_id, name):
        return Ticket(user_id=user_id, name=name, status=TICKET_STATUS[0])

    def get_ticket_page_count(self, ticket_queryset):
        return math.ceil(len(ticket_queryset) / TICKET_PAGE_COUNT)

    def get_all_tickets(self, page, user_type):
        end_limit = page * TICKET_PAGE_COUNT
        start_limit = end_limit - TICKET_PAGE_COUNT

        ticket_queryset = Ticket.query.filter_by(name=user_type, status=TICKET_STATUS[0]).all()

        page_count = self.get_ticket_page_count(ticket_queryset)

        tickets = ticket_queryset[start_limit:end_limit]

        ticket_list = []
        for ticket in tickets:
            context = {
                "id": ticket.user_id,
                "created_at": ticket.created_at,
            }

            ticket_list.append(context)

        return ticket_list, page_count

    def get_ticket_query(self, id):
        return Ticket.query.filter_by(user_id=id).first()

    def get_action_status(self, action):
        return TICKET_STATUS[1] if action == TICKET_ACTION[0] else TICKET_STATUS[2]
