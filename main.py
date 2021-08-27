from app.app import app
from user.views import user_bp
from owner.views import owner_bp
from agent.views import agent_bp
from ticket.views import ticket_bp
from profile.views import profile_bp
from activity.views import activity_bp


app.register_blueprint(user_bp)
app.register_blueprint(owner_bp)
app.register_blueprint(agent_bp)
app.register_blueprint(ticket_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(activity_bp)


if __name__ == "__main__":
    app.run()
