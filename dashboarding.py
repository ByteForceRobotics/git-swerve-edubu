import wpilib
import ntcore
class Dashboarding:
    def __init__(self):
        """Initialize the Dashboarding class."""
        self.table = ntcore.NetworkTableInstance.getDefault().getTable("SmartDashboard")
        

    def update_dashboard(self,name, data):
        """
        Update the dashboard with the provided data.

        Args:
            data (dict): A dictionary containing the data to update.
        """
        self.table.putNumber(name, data)

    def reset_dashboard(self):
        """Reset the dashboard to its default state."""
        pass