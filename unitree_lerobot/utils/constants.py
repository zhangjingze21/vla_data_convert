import dataclasses


@dataclasses.dataclass(frozen=True)
class RobotConfig:
    motors: list[str]
    cameras: list[str]
    camera_to_image_key: dict[str, str]
    json_state_data_name: list[str]
    json_action_data_name: list[str]
    state_names: list[str] | None = None  # Optional separate state names if different from motors


Z1_CONFIG = RobotConfig(
    motors=[
        "kLeftWaist",
        "kLeftShoulder",
        "kLeftElbow",
        "kLeftForearmRoll",
        "kLeftWristAngle",
        "kLeftWristRotate",
        "kLeftGripper",
        "kRightWaist",
        "kRightShoulder",
        "kRightElbow",
        "kRightForearmRoll",
        "kRightWristAngle",
        "kRightWristRotate",
        "kRightGripper",
    ],
    cameras=[
        "cam_high",
        "cam_left_wrist",
        "cam_right_wrist",
    ],
    camera_to_image_key={"color_0": "cam_high", "color_1": "cam_left_wrist", "color_2": "cam_right_wrist"},
    json_state_data_name=["left_arm.qpos", "right_arm.qpos"],
    json_action_data_name=["left_arm.qpos", "right_arm.qpos"],
)


Z1_SINGLE_CONFIG = RobotConfig(
    motors=[
        "kWaist",
        "kShoulder",
        "kElbow",
        "kForearmRoll",
        "kWristAngle",
        "kWristRotate",
        "kGripper",
    ],
    cameras=[
        "cam_high",
        "cam_wrist",
    ],
    camera_to_image_key={"color_0": "cam_high", "color_1": "cam_wrist"},
    json_state_data_name=["left_arm.qpos", "right_arm.qpos"],
    json_action_data_name=["left_arm.qpos", "right_arm.qpos"],
)


G1_DEX1_CONFIG = RobotConfig(
    motors=[
        "kLeftShoulderPitch",
        "kLeftShoulderRoll",
        "kLeftShoulderYaw",
        "kLeftElbow",
        "kLeftWristRoll",
        "kLeftWristPitch",
        "kLeftWristYaw",
        "kRightShoulderPitch",
        "kRightShoulderRoll",
        "kRightShoulderYaw",
        "kRightElbow",
        "kRightWristRoll",
        "kRightWristPitch",
        "kRightWristYaw",
        "kLeftGripper",
        "kRightGripper",
    ],
    cameras=[
        "cam_left_high",
        "cam_right_high",
        "cam_left_wrist",
        "cam_right_wrist",
    ],
    camera_to_image_key={
        "color_0": "cam_left_high",
        "color_1": "cam_right_high",
        "color_2": "cam_left_wrist",
        "color_3": "cam_right_wrist",
    },
    json_state_data_name=["left_arm.qpos", "right_arm.qpos", "left_ee.qpos", "right_ee.qpos"],
    json_action_data_name=["left_arm.qpos", "right_arm.qpos", "left_ee.qpos", "right_ee.qpos"],
)


G1_DEX1_CONFIG_SIM = RobotConfig(
    motors=[
        "kLeftShoulderPitch",
        "kLeftShoulderRoll",
        "kLeftShoulderYaw",
        "kLeftElbow",
        "kLeftWristRoll",
        "kLeftWristPitch",
        "kLeftWristYaw",
        "kRightShoulderPitch",
        "kRightShoulderRoll",
        "kRightShoulderYaw",
        "kRightElbow",
        "kRightWristRoll",
        "kRightWristPitch",
        "kRightWristYaw",
        "kLeftGripper",
        "kRightGripper",
    ],
    cameras=[
        "cam_left_high",
        "cam_left_wrist",
        "cam_right_wrist",
    ],
    camera_to_image_key={
        "color_0": "cam_left_high",
        "color_1": "cam_left_wrist",
        "color_2": "cam_right_wrist",
    },
    json_state_data_name=["left_arm.qpos", "right_arm.qpos", "left_ee.qpos", "right_ee.qpos"],
    json_action_data_name=["left_arm.qpos", "right_arm.qpos", "left_ee.qpos", "right_ee.qpos"],
)


G1_DEX3_CONFIG = RobotConfig(
    motors=[
        "kLeftShoulderPitch",
        "kLeftShoulderRoll",
        "kLeftShoulderYaw",
        "kLeftElbow",
        "kLeftWristRoll",
        "kLeftWristPitch",
        "kLeftWristYaw",
        "kRightShoulderPitch",
        "kRightShoulderRoll",
        "kRightShoulderYaw",
        "kRightElbow",
        "kRightWristRoll",
        "kRightWristPitch",
        "kRightWristYaw",
        "kLeftHandThumb0",
        "kLeftHandThumb1",
        "kLeftHandThumb2",
        "kLeftHandMiddle0",
        "kLeftHandMiddle1",
        "kLeftHandIndex0",
        "kLeftHandIndex1",
        "kRightHandThumb0",
        "kRightHandThumb1",
        "kRightHandThumb2",
        "kRightHandIndex0",
        "kRightHandIndex1",
        "kRightHandMiddle0",
        "kRightHandMiddle1",
    ],
    cameras=[
        "cam_left_high",
        "cam_right_high",
        "cam_left_wrist",
        "cam_right_wrist",
    ],
    camera_to_image_key={
        "color_0": "cam_left_high",
        "color_1": "cam_right_high",
        "color_2": "cam_left_wrist",
        "color_3": "cam_right_wrist",
    },
    json_state_data_name=["left_arm.qpos", "right_arm.qpos", "left_ee.qpos", "right_ee.qpos"],
    json_action_data_name=["left_arm.qpos", "right_arm.qpos", "left_ee.qpos", "right_ee.qpos"],
)


G1_BRAINCO_CONFIG = RobotConfig(
    motors=[
        "kLeftShoulderPitch",
        "kLeftShoulderRoll",
        "kLeftShoulderYaw",
        "kLeftElbow",
        "kLeftWristRoll",
        "kLeftWristPitch",
        "kLeftWristYaw",
        "kRightShoulderPitch",
        "kRightShoulderRoll",
        "kRightShoulderYaw",
        "kRightElbow",
        "kRightWristRoll",
        "kRightWristPitch",
        "kRightWristYaw",
        "kLeftHandThumb",
        "kLeftHandThumbAux",
        "kLeftHandIndex",
        "kLeftHandMiddle",
        "kLeftHandRing",
        "kLeftHandPinky",
        "kRightHandThumb",
        "kRightHandThumbAux",
        "kRightHandIndex",
        "kRightHandMiddle",
        "kRightHandRing",
        "kRightHandPinky",
    ],
    cameras=[
        "cam_left_high",
        "cam_right_high",
        "cam_left_wrist",
        "cam_right_wrist",
    ],
    camera_to_image_key={
        "color_0": "cam_left_high",
        "color_1": "cam_right_high",
        "color_2": "cam_left_wrist",
        "color_3": "cam_right_wrist",
    },
    json_state_data_name=["left_arm.qpos", "right_arm.qpos", "left_ee.qpos", "right_ee.qpos"],
    json_action_data_name=["left_arm.qpos", "right_arm.qpos", "left_ee.qpos", "right_ee.qpos"],
)


G1_INSPIRE_CONFIG = RobotConfig(
    motors=[
        "kLeftShoulderPitch",
        "kLeftShoulderRoll",
        "kLeftShoulderYaw",
        "kLeftElbow",
        "kLeftWristRoll",
        "kLeftWristPitch",
        "kLeftWristYaw",
        "kRightShoulderPitch",
        "kRightShoulderRoll",
        "kRightShoulderYaw",
        "kRightElbow",
        "kRightWristRoll",
        "kRightWristPitch",
        "kRightWristYaw",
        "kLeftHandPinky",
        "kLeftHandRing",
        "kLeftHandMiddle",
        "kLeftHandIndex",
        "kLeftHandThumbBend",
        "kLeftHandThumbRotation",
        "kRightHandPinky",
        "kRightHandRing",
        "kRightHandMiddle",
        "kRightHandIndex",
        "kRightHandThumbBend",
        "kRightHandThumbRotation",
    ],
    cameras=[
        "cam_left_high",
        "cam_right_high",
        "cam_left_wrist",
        "cam_right_wrist",
    ],
    camera_to_image_key={
        "color_0": "cam_left_high",
        "color_1": "cam_right_high",
        "color_2": "cam_left_wrist",
        "color_3": "cam_right_wrist",
    },
    json_state_data_name=["left_arm.qpos", "right_arm.qpos", "left_ee.qpos", "right_ee.qpos"],
    json_action_data_name=["left_arm.qpos", "right_arm.qpos", "left_ee.qpos", "right_ee.qpos"],
)


G1_INSPIRE_SINGLE_CAM_CONFIG = RobotConfig(
    motors=[
        "kLeftShoulderPitch",
        "kLeftShoulderRoll",
        "kLeftShoulderYaw",
        "kLeftElbow",
        "kLeftWristRoll",
        "kLeftWristPitch",
        "kLeftWristYaw",
        "kRightShoulderPitch",
        "kRightShoulderRoll",
        "kRightShoulderYaw",
        "kRightElbow",
        "kRightWristRoll",
        "kRightWristPitch",
        "kRightWristYaw",
        "kLeftHandPinky",
        "kLeftHandRing",
        "kLeftHandMiddle",
        "kLeftHandIndex",
        "kLeftHandThumbBend",
        "kLeftHandThumbRotation",
        "kRightHandPinky",
        "kRightHandRing",
        "kRightHandMiddle",
        "kRightHandIndex",
        "kRightHandThumbBend",
        "kRightHandThumbRotation",
        # "KHeadCameraYaw",
        # "KHeadCameraPitch"
    ],
    cameras=[
        "cam_high",
    ],
    camera_to_image_key={
        "color_0": "cam_high",
    },
    json_state_data_name=["left_arm.qpos", "right_arm.qpos", "left_ee.qpos", "right_ee.qpos"],
    json_action_data_name=["left_arm.qpos", "right_arm.qpos", "left_ee.qpos", "right_ee.qpos"],
)

G1_INSPIRE_WHOLEBODY = RobotConfig(
    # motors defines the action space (64 dimensions)
    motors=[
        # task_obs.mocap_body_quat[-1] (4)
        "mocap_body_quat_w", "mocap_body_quat_x", "mocap_body_quat_y", "mocap_body_quat_z",
        
        # task_obs.mocap_root_lin_vel[-1] (3)
        "mocap_root_lin_vel_x", "mocap_root_lin_vel_y", "mocap_root_lin_vel_z",
        
        # task_obs.mocap_qpos (36)
        "mocap_qpos_0", "mocap_qpos_1", "mocap_qpos_2", "mocap_qpos_3", "mocap_qpos_4", "mocap_qpos_5",
        "mocap_qpos_6", "mocap_qpos_7", "mocap_qpos_8", "mocap_qpos_9", "mocap_qpos_10", "mocap_qpos_11", 
        "mocap_qpos_12", "mocap_qpos_13", "mocap_qpos_14", "mocap_qpos_15", "mocap_qpos_16", "mocap_qpos_17", 
        "mocap_qpos_18", "mocap_qpos_19", "mocap_qpos_20", "mocap_qpos_21", "mocap_qpos_22", "mocap_qpos_23", 
        "mocap_qpos_24", "mocap_qpos_25", "mocap_qpos_26", "mocap_qpos_27", "mocap_qpos_28", "mocap_qpos_29", 
        "mocap_qpos_30", "mocap_qpos_31", "mocap_qpos_32", "mocap_qpos_33", "mocap_qpos_34", "mocap_qpos_35",
        
        # task_obs.mocap_relative_root_quat (4)
        "mocap_rel_root_quat_w", "mocap_rel_root_quat_x", "mocap_rel_root_quat_y", "mocap_rel_root_quat_z",

        # left_hand.qpos (6)
        "kLeftHandPinky",
        "kLeftHandRing",
        "kLeftHandMiddle",
        "kLeftHandIndex",
        "kLeftHandThumbBend",
        "kLeftHandThumbRotation",

        # right_hand.qpos (6)

        "kRightHandPinky",
        "kRightHandRing",
        "kRightHandMiddle",
        "kRightHandIndex",
        "kRightHandThumbBend",  
        "kRightHandThumbRotation",

        # head_servo.qpos (2)
        "kHeadPitch",
        "kHeadYaw",

        # pelvis xyz delta relative to the first frame (3)
        "pelvis_xyz_delta_x",
        "pelvis_xyz_delta_y",
        "pelvis_xyz_delta_z",
    ],

    # state_names defines the observation state space (79 dimensions)
    state_names=[
        # left arm qpos (7)
        "kLeftShoulderPitch",
        "kLeftShoulderRoll",
        "kLeftShoulderYaw",
        "kLeftElbow",
        "kLeftWristRoll",
        "kLeftWristPitch",
        "kLeftWristYaw",
        # left arm qvel (7)
        "kLeftShoulderPitchVel",
        "kLeftShoulderRollVel",
        "kLeftShoulderYawVel",
        "kLeftElbowVel",
        "kLeftWristRollVel",
        "kLeftWristPitchVel",
        "kLeftWristYawVel",
        
        # right arm qpos (7)
        "kRightShoulderPitch",
        "kRightShoulderRoll",
        "kRightShoulderYaw",
        "kRightElbow",
        "kRightWristRoll",
        "kRightWristPitch",
        "kRightWristYaw",
        # right arm qvel (7)
        "kRightShoulderPitchVel",
        "kRightShoulderRollVel",
        "kRightShoulderYawVel",
        "kRightElbowVel",
        "kRightWristRollVel",
        "kRightWristPitchVel",
        "kRightWristYawVel",
        
        # left hand qpos (6)
        "kLeftHandPinky",
        "kLeftHandRing",
        "kLeftHandMiddle",
        "kLeftHandIndex",
        "kLeftHandThumbBend",
        "kLeftHandThumbRotation",
        
        # right hand qpos (6)
        "kRightHandPinky",
        "kRightHandRing",
        "kRightHandMiddle",
        "kRightHandIndex",
        "kRightHandThumbBend",
        "kRightHandThumbRotation",
        
        # waist qpos (3)
        "kWaistYaw",
        "kWaistRoll",
        "kWaistPitch",
        # waist qvel (3)
        "kWaistYawVel",
        "kWaistRollVel",
        "kWaistPitchVel",
        
        # left leg qpos (6)
        "kLeftHipPitch",
        "kLeftHipRoll",
        "kLeftHipYaw",
        "kLeftKnee",
        "kLeftAnklePitch",
        "kLeftAnkleRoll",
        # left leg qvel (6)
        "kLeftHipPitchVel",
        "kLeftHipRollVel",
        "kLeftHipYawVel",
        "kLeftKneeVel",
        "kLeftAnklePitchVel",
        "kLeftAnkleRollVel",
        
        # right leg qpos (6)
        "kRightHipPitch",
        "kRightHipRoll",
        "kRightHipYaw",
        "kRightKnee",
        "kRightAnklePitch",
        "kRightAnkleRoll",
        # right leg qvel (6)
        "kRightHipPitchVel",
        "kRightHipRollVel",
        "kRightHipYawVel",
        "kRightKneeVel",
        "kRightAnklePitchVel",
        "kRightAnkleRollVel",
        
        # imu ang_vel (3)
        "kBodyAngVelRoll",
        "kBodyAngVelPitch",
        "kBodyAngVelYaw",
        # imu quat (4)
        "kBodyQuatW",
        "kBodyQuatX",
        "kBodyQuatY",
        "kBodyQuatZ",
        
        # head_servo qpos (2)
        "kHeadPitch",
        "kHeadYaw",
    ],
    cameras=[
        "cam_high",
    ],
    camera_to_image_key={
        "color_0": "cam_high",
    },
    # state: left_arm(7+7) + right_arm(7+7) + left_hand(6) + right_hand(6) + waist(3+3) + left_leg(6+6) + right_leg(6+6) + imu(3+4) + head_servo(2) = 79
    # todo: hands & head use last action
    json_state_data_name=["left_arm.qpos", "left_arm.qvel", "right_arm.qpos", "right_arm.qvel", "left_hand.qpos", "right_hand.qpos", "waist.qpos", "waist.qvel", "left_leg.qpos", "left_leg.qvel", "right_leg.qpos", "right_leg.qvel", "imu.ang_vel", "imu.quat", "head_servo.qpos"],
    # action: task_obs[mocap_body_quat[-1], mocap_root_lin_vel[-1], mocap_qpos, mocap_relative_root_quat]
    json_action_data_name=["task_obs.mocap_body_quat[-1][0]", "task_obs.mocap_root_lin_vel[-1]", "task_obs.mocap_qpos", "task_obs.mocap_relative_root_quat", "left_hand.qpos", "right_hand.qpos", "head_servo.qpos"],
)


MOVEIBLE_LIFT_G1_DEX1_USEWAIST_CONFIG = RobotConfig(
    motors=[
        "kLeftShoulderPitch",
        "kLeftShoulderRoll",
        "kLeftShoulderYaw",
        "kLeftElbow",
        "kLeftWristRoll",
        "kLeftWristPitch",
        "kLeftWristYaw",
        "kRightShoulderPitch",
        "kRightShoulderRoll",
        "kRightShoulderYaw",
        "kRightElbow",
        "kRightWristRoll",
        "kRightWristPitch",
        "kRightWristYaw",
        "kWaistYaw",
        "kWaistPitch",
        "kHighLift",
        "kMoveX",
        "kMoveYaw",
        "kLeftGripper",
        "kRightGripper",
    ],
    cameras=[
        "cam_left_high",
        "cam_right_high",
        "cam_left_wrist",
        "cam_right_wrist",
    ],
    camera_to_image_key={
        "color_0": "cam_left_high",
        "color_1": "cam_right_high",
        "color_2": "cam_left_wrist",
        "color_3": "cam_right_wrist",
    },
    json_state_data_name=[
        "left_arm.qpos",
        "right_arm.qpos",
        "waist.qpos",
        "torso.height",
        "chassis.qvel",
        "left_ee.qpos",
        "right_ee.qpos",
    ],
    json_action_data_name=[
        "left_arm.qpos",
        "right_arm.qpos",
        "waist.qpos",
        "torso.qvel",
        "chassis.qvel",
        "left_ee.qpos",
        "right_ee.qpos",
    ],
)


MOVEIBLE_LIFT_G1_DEX1_NOUSEWAIST_CONFIG = RobotConfig(
    motors=[
        "kLeftShoulderPitch",
        "kLeftShoulderRoll",
        "kLeftShoulderYaw",
        "kLeftElbow",
        "kLeftWristRoll",
        "kLeftWristPitch",
        "kLeftWristYaw",
        "kRightShoulderPitch",
        "kRightShoulderRoll",
        "kRightShoulderYaw",
        "kRightElbow",
        "kRightWristRoll",
        "kRightWristPitch",
        "kRightWristYaw",
        "kHighLift",
        "kMoveX",
        "kMoveYaw",
        "kLeftGripper",
        "kRightGripper",
    ],
    cameras=[
        "cam_left_high",
        "cam_right_high",
        "cam_left_wrist",
        "cam_right_wrist",
    ],
    camera_to_image_key={
        "color_0": "cam_left_high",
        "color_1": "cam_right_high",
        "color_2": "cam_left_wrist",
        "color_3": "cam_right_wrist",
    },
    json_state_data_name=[
        "left_arm.qpos",
        "right_arm.qpos",
        "torso.height",
        "chassis.qvel",
        "left_ee.qpos",
        "right_ee.qpos",
    ],
    json_action_data_name=[
        "left_arm.qpos",
        "right_arm.qpos",
        "torso.qvel",
        "chassis.qvel",
        "left_ee.qpos",
        "right_ee.qpos",
    ],
)


LIFT_G1_DEX1_USEWAIST_CONFIG = RobotConfig(
    motors=[
        "kLeftShoulderPitch",
        "kLeftShoulderRoll",
        "kLeftShoulderYaw",
        "kLeftElbow",
        "kLeftWristRoll",
        "kLeftWristPitch",
        "kLeftWristYaw",
        "kRightShoulderPitch",
        "kRightShoulderRoll",
        "kRightShoulderYaw",
        "kRightElbow",
        "kRightWristRoll",
        "kRightWristPitch",
        "kRightWristYaw",
        "kWaistYaw",
        "kWaistRoll",
        "kHighLift",
        "kLeftGripper",
        "kRightGripper",
    ],
    cameras=[
        "cam_left_high",
        "cam_right_high",
        "cam_left_wrist",
        "cam_right_wrist",
    ],
    camera_to_image_key={
        "color_0": "cam_left_high",
        "color_1": "cam_right_high",
        "color_2": "cam_left_wrist",
        "color_3": "cam_right_wrist",
    },
    json_state_data_name=[
        "left_arm.qpos",
        "right_arm.qpos",
        "waist.qpos",
        "torso.height",
        "left_ee.qpos",
        "right_ee.qpos",
    ],
    json_action_data_name=[
        "left_arm.qpos",
        "right_arm.qpos",
        "waist.qpos",
        "torso.qvel",
        "left_ee.qpos",
        "right_ee.qpos",
    ],
)


LIFT_G1_DEX1_NOUSEWAIST_CONFIG = RobotConfig(
    motors=[
        "kLeftShoulderPitch",
        "kLeftShoulderRoll",
        "kLeftShoulderYaw",
        "kLeftElbow",
        "kLeftWristRoll",
        "kLeftWristPitch",
        "kLeftWristYaw",
        "kRightShoulderPitch",
        "kRightShoulderRoll",
        "kRightShoulderYaw",
        "kRightElbow",
        "kRightWristRoll",
        "kRightWristPitch",
        "kRightWristYaw",
        "kHighLift",
        "kLeftGripper",
        "kRightGripper",
    ],
    cameras=[
        "cam_left_high",
        "cam_right_high",
        "cam_left_wrist",
        "cam_right_wrist",
    ],
    camera_to_image_key={
        "color_0": "cam_left_high",
        "color_1": "cam_right_high",
        "color_2": "cam_left_wrist",
        "color_3": "cam_right_wrist",
    },
    json_state_data_name=["left_arm.qpos", "right_arm.qpos", "torso.height", "left_ee.qpos", "right_ee.qpos"],
    json_action_data_name=["left_arm.qpos", "right_arm.qpos", "torso.qvel", "left_ee.qpos", "right_ee.qpos"],
)

ROBOT_CONFIGS = {
    "Unitree_Z1_Single": Z1_SINGLE_CONFIG,
    "Unitree_Z1_Dual": Z1_CONFIG,
    "Unitree_G1_Dex1": G1_DEX1_CONFIG,
    "Unitree_G1_Dex1_Sim": G1_DEX1_CONFIG_SIM,
    "Unitree_G1_Dex3": G1_DEX3_CONFIG,
    "Unitree_G1_Brainco": G1_BRAINCO_CONFIG,
    "Unitree_G1_Inspire": G1_INSPIRE_CONFIG,
    "Unitree_G1_Inspire_SingleCam": G1_INSPIRE_SINGLE_CAM_CONFIG,
    "Unitree_G1_MoveibleLift_Dex1_UseWaist": MOVEIBLE_LIFT_G1_DEX1_USEWAIST_CONFIG,
    "Unitree_G1_MoveibleLift_Dex1_NoUseWaist": MOVEIBLE_LIFT_G1_DEX1_NOUSEWAIST_CONFIG,
    "Unitree_G1_Lift_Dex1_UseWaist": LIFT_G1_DEX1_USEWAIST_CONFIG,
    "Unitree_G1_Lift_Dex1_NoUseWaist": LIFT_G1_DEX1_NOUSEWAIST_CONFIG,
    "Unitree_G1_Inspire_wholebody": G1_INSPIRE_WHOLEBODY,
}
