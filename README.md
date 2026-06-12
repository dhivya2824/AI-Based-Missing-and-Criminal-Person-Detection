# AI-Based-Missing-and-Criminal-Person-Detection


ackage Installation Summary
✅ Successfully Installed Packages
The following packages have been successfully installed:

Django==5.0.6 - Web framework
numpy - Numerical computing
joblib - Serialization library
Pillow - Image processing
opencv-python - Computer vision
geocoder - Location services
twilio - SMS notifications
nltk - Natural language processing
gtts - Text-to-speech
googletrans==4.0.0rc1 - Translation
pyttsx3 - Text-to-speech engine
pygame - Audio playback
⚠️ Packages Requiring Additional Setup
1. matplotlib & seaborn
Issue: Requires C++ compiler (Visual Studio Build Tools)

Solution:

Install Microsoft Visual C++ Build Tools from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
Then run: pip install matplotlib seaborn
2. face-recognition
Issue: Requires dlib which needs CMake

Solution:

Install CMake from: https://cmake.org/download/
Install Visual Studio Build Tools (same as above)
Then run: pip install face-recognition
3. tensorflow & keras
Issue: Not available for 32-bit Python

Solution:

Install 64-bit Python 3.10
Create a new virtual environment with 64-bit Python
Then run: pip install tensorflow keras
🔧 System Information
Python Version: 3.10.3 (32-bit)
Operating System: Windows
📝 Next Steps
For face detection to work: Install face-recognition package after setting up CMake and Visual Studio Build Tools
For chatbot to work: Install tensorflow and keras (requires 64-bit Python)
For data visualization: Install matplotlib and seaborn (requires Visual Studio Build Tools)
🚀 Running the Project
After installing the missing packages, you can run the project with:

python manage.py runserver
📌 Important Notes
The project uses face recognition for missing person detection
The chatbot requires TensorFlow/Keras models
Some features may not work without the packages that require additional setup
