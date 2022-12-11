#!/usr/bin/python3

import rospy
import tf
from moveit_commander.planning_scene_interface import PlanningSceneInterface
import tf2_ros

import math

from geometry_msgs.msg import TransformStamped
from scorpius_manipulation.srv import SceneUpdate, SceneUpdateResponse, SceneUpdateRequest
from scorpius_manipulation.msg import SceneObject

from archie_manipulation.srv import Pick, PickRequest, PickResponse
from archie_manipulation.srv import Place, PlaceRequest, PlaceResponse

import manipulator

sceneUpdateService = None
arm = None
scene = None

def pickUp(request: PickRequest) -> PickResponse:
    sceneRequest = SceneUpdateRequest()
    sceneRequest.fixedFrame.data = 'map'
    sceneResponse:SceneUpdateResponse
    sceneResponse = sceneUpdateService.call(sceneRequest)

    arm.pick(request.objectName.data)
    arm.goToHoldingPose()

    return PickResponse()

def placeDown(request: PlaceRequest) -> PlaceResponse:
    arm.place(request.objectName.data)
    arm.goToHomePose()
    scene.remove_attached_object(request.objectName.data)
    scene.remove_world_object(request.objectName.data)

    return PlaceResponse()

if __name__ == "__main__":
    rospy.init_node('archie_manipulation', anonymous=False)

    sceneUpdateService = rospy.ServiceProxy(
            'scene_update_service', SceneUpdate)
    arm = manipulator.Manipulator('sting_arm')
    scene = PlanningSceneInterface()

    pickService = rospy.Service('pick_service', Pick, pickUp)
    placeService = rospy.Service('pick_service', Place, placeDown)

    rospy.spin()

    # request = PickRequest()
    # request.objectName = 'cup1'
    # pick_Up(request)

    # request = PlaceRequest()
    # request.objectName = 'cup1'
    # placeDown(request)


    # object: SceneObject
    # for object in response.objects.objects:
    #     objectName = object.name
    #     arm.pickAndPlace(objectName, "place")
    #     rospy.sleep(0.1)
    #     scene.remove_world_object(objectName)
    #     rospy.sleep(0.5)