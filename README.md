# VVC_CU_Partition_Visualization
VVC_CU_Partition_Visualization
![image](https://github.com/Huai0429/VVC_CU_Partition_Visualization/blob/main/CTU000.png)
# Cpp file
add the following code at the end of "compressCTU" function
## CU
```
int ctuindex = 1,frame_idx = 1;  
std::string filename = std::to_string(ctuindex);
std::ofstream myfile;
std::string Path  = "./CTUinfo/BasketBallPass/frame"+std::to_string(frame_idx);
std::experimental::filesystem::create_directory(Path);
myfile.open(Path+"/CTU_" + std::to_string(ctuindex++) + ".txt");
for (auto &currCU : cs.traverseCUs(area, ChannelType::LUMA))
{
    const CompArea&  lumaArea = currCU.block(COMPONENT_Y);
    int cuX = lumaArea.x;
    int cuY = lumaArea.y;
    int cuH = lumaArea.height;
    int cuW = lumaArea.width;
    std::string info = "";


    info = std::to_string(cuX) + " " + std::to_string(cuY) + " " + std::to_string(cuH) +" "+ std::to_string(cuW) +"\n";
    myfile << info;


}
if (ctuindex==9) {frame_idx++;ctuindex = 1;}
myfile.close();
```
## TU (non tested)
```
std::ofstream TUmyfile;
TUmyfile.open(Path+"/TU_" + std::to_string(ctuindex) + ".txt");
for (auto &currCU : cs.traverseCUs(area, ChannelType::LUMA))
{
    for (auto &currTU : CU::traverseTUs(currCU))
    {

        const CompArea&  lumaArea = currTU.block(COMPONENT_Y);
        int cuX = lumaArea.x;
        int cuY = lumaArea.y;
        int cuH = lumaArea.height;
        int cuW = lumaArea.width;
        int mtsidx = currTU.mtsIdx;
        std::string info = "";
        info = std::to_string(cuX) + " " + std::to_string(cuY) + " " + std::to_string(cuH) + " " + std::to_string(cuW) + " " + std::to_string(mtsidx) + "\n";
        TUmyfile << info;
    }
}
TUmyfile.close();
```
# Python file 
using python Visual.py -h for more useful information
