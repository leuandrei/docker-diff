import subprocess
import argparse

parser=argparse.ArgumentParser()

parser.add_argument('--first-image', help='Name of a docker image', required=True)
parser.add_argument('--second-image', help='Name of anoter docker image', required=True)

args=parser.parse_args()

print(args)


def generatePackageList(dockerImage):
    p = subprocess.check_output(["syft", dockerImage])
    out = p.decode("utf-8")

    # Obtain package list from the syft output, after removing the header
    packageList = out.split()[3:]

    packageDict = dict()

    for i in range(0, len(packageList) - 1, 3):
        packageDict[packageList[i]] = [packageList[i + 1], packageList[i + 2]]

    return packageDict

def uniquePackages(pkgList, commonPkgs):
    for package in pkgList:
        if package not in commonPkgs.keys():
            print(package, pkgList[package][0], pkgList[package][1])

def packageDiff(list1, list2):
    commonPackages = dict()
    for package in list1:
        for item in list2:
            if package == item:
                if list1[package] == list2[item]:
                    commonPackages[package] = list1[package]
                    break
                else:
                    print("Package {} has been changed:"
                          "\n{} Version:{} Type:{}"
                          "\n{} Version:{} Type:{}\n"
                          .format(package, args.first_image, list1[package][0], list1[package][1],
                                           args.second_image, list2[item][0], list2[item][1]))
    print("Packages found only on {}:".format(args.first_image))
    uniquePackages(list1, commonPackages)
    print("Packages found only on {}:".format(args.second_image))
    uniquePackages(list2, commonPackages)

print("Identifying packages for {}".format(args.first_image))
firstPackageList = generatePackageList(args.first_image)
print("Identifying packages for {}".format(args.second_image))
secondPackageList = generatePackageList(args.second_image)
print("Starting package diff..")
packageDiff(firstPackageList, secondPackageList)
