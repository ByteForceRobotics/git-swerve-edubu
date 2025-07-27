import wpilib
import wpimath
import wpilib.drive
import wpimath.filter
import wpimath.controller
import navx
import drivesubsystem
import dashboarding
from ntcore import NetworkTableInstance
import constants

# To see messages from networktables, you must setup logging
import logging

logging.basicConfig(level=logging.DEBUG)

class MyRobot(wpilib.TimedRobot):
    def robotInit(self) -> None:
        """Robot initialization function"""
        self.driverController = wpilib.XboxController(constants.kDriverControllerPort)
        
        self.swerve = drivesubsystem.DriveSubsystem()

        # Slew rate limiters to make joystick inputs more gentle; 1/3 sec from 0 to 1.
        self.xspeedLimiter = wpimath.filter.SlewRateLimiter(3)
        self.yspeedLimiter = wpimath.filter.SlewRateLimiter(3)
        self.rotLimiter = wpimath.filter.SlewRateLimiter(3)
        
        self.table = dashboarding.Dashboarding() 
        
        #self.table.putNumber("RobotInitTime",wpilib.Timer.getFPGATimestamp())
    
    def autonomousInit(self) -> None:
        pass

    def autonomousPeriodic(self) -> None:
        pass

    def teleopInit(self) -> None:
        pass
    

    def teleopPeriodic(self) -> None:
        # Teleop periodic logic
        self.driveWithJoystick(False)
        self.table.update_dashboard("test",1)
        self.table.update_dashboard("frontleft output current",self.swerve.frontLeft.drivingSparkMax.getOutputCurrent())
        
        self.table.update_dashboard("leftY", self.driverController.getLeftY())
        self.table.update_dashboard("leftX", self.driverController.getLeftX())
        self.table.update_dashboard("rightY", self.driverController.getRightY())
        self.table.update_dashboard("getPosFL", self.swerve.frontLeft.drivingEncoder.getPosition())
        self.table.update_dashboard("getPosFR", self.swerve.frontRight.drivingEncoder.getPosition())
        self.table.update_dashboard("getPosRL", self.swerve.rearLeft.drivingEncoder.getPosition())
        self.table.update_dashboard("getPosRR", self.swerve.rearRight.drivingEncoder.getPosition())
        # self.table.update_dashboard("setPos", self.swerve.frontLeft.drivingEncoder.setPosition())
        self.table.update_dashboard("getVelo", self.swerve.frontLeft.drivingEncoder.getVelocity())
        

    
    def testPeriodic(self) -> None:
        pass

    def driveWithJoystick(self, fieldRelative: bool) -> None:
        # Get the x speed. We are inverting this because Xbox controllers return
        # negative values when we push forward.
        xSpeed = (
            -self.xspeedLimiter.calculate(
                wpimath.applyDeadband(self.driverController.getLeftY(), 0.08)
            )
            * constants.kMaxSpeed
        )
        # xSpeed = (self.driverController.getLeftY() * constants.kMaxSpeed)

        # Get the y speed or sideways/strafe speed. We are inverting this because
        # we want a positive value when we pull to the left. Xbox controllers
        # return positive values when you pull to the right by default.
        ySpeed = (
            -self.yspeedLimiter.calculate(
                wpimath.applyDeadband(self.driverController.getLeftX(), 0.08)
            )
            * constants.kMaxSpeed
        )

        # ySpeed = 0

        # Get the rate of angular rotation. We are inverting this because we want a
        # positive value when we pull to the left (remember, CCW is positive in
        # mathematics). Xbox controllers return positive values when you pull to
        # the right by default.
        rot = (
            -self.rotLimiter.calculate(
                wpimath.applyDeadband(self.driverController.getRightX(), 0.08)
            )
            * constants.kMaxSpeed
        )
        # rot = 0

        self.swerve.drive(xSpeed, ySpeed, rot, fieldRelative, rateLimit=False)

if __name__ == "__main__":
    wpilib.run(MyRobot)