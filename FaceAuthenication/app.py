import cv2
import boto3
from flask import Flask, render_template, redirect, request
import flask
app = Flask(__name__)




# Delete previous image used for the face verification
@app.route('/delete')
def delete(s3, client):
    myBucket = s3.Bucket('faceverifyproject')
    for obj in myBucket.objects.all():
        if obj.key != 'IMG_Reference.jpeg':
            verificationImage = obj.key
    referenceImage = 'IMG_Reference.jpeg'
    client.delete_object(Bucket='faceverifyproject',Key=verificationImage)
    return referenceImage

# Call the AWS Face compare API
@app.route('/compare')
def compare_faces(referenceImage, verificationImage):

    client=boto3.client('rekognition')
   
    imageSource=open(referenceImage,'rb')
    imageTarget=open(verificationImage,'rb')
    
    # Determine whether both images contain faces
    try:
        response=client.compare_faces(SimilarityThreshold=80,
                                    SourceImage={'Bytes': imageSource.read()},
                                    TargetImage={'Bytes': imageTarget.read()})
    
    # Return 0 if one of the images does not have a face in it
    except:
        return '0 faces were detected'
    
    for faceMatch in response['FaceMatches']:
        position = faceMatch['Face']['BoundingBox']
        similarity = str(faceMatch['Similarity'])
        print('The face at ' +
               str(position['Left']) + ' ' +
               str(position['Top']) +
               ' matches with ' + similarity + '% confidence')
    imageSource.close()
    imageTarget.close()     
    return len(response['FaceMatches'])          

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/main')
def main():
        
    # Call the OpenCV application to take a picture
    verificationImage = camera()
        
    # Delete the previously uploaded image
    s3 = boto3.resource('s3')
    client = boto3.client('s3')
    reference = delete(s3, client)
    
    # Store the image that was retrieved from the camera
    with open("Verification.jpeg",'rb') as data:
        client.upload_fileobj(data, 'faceverifyproject','Verification.jpeg')
    
    # Compare the two images that are pulled from the s3 bucket
    face_matches=compare_faces(reference, verificationImage)
    return "Face matches: " + str(face_matches)


@app.post('/api')
def api():
    
    image = flask.request.files.get('image')
    image.save('Verification.jpeg')
    
    verificationImage = 'Verification.jpeg'
    
    # Delete the previously uploaded image
    s3 = boto3.resource('s3')
    client = boto3.client('s3')

    try:
        reference = delete(s3, client)
    except:
        reference = 'IMG_Reference.jpeg'
    
    # Store the image that was retrieved from the camera
    with open("Verification.jpeg",'rb') as data:
        client.upload_fileobj(data, 'faceverifyproject', 'Verification.jpeg')
    
    # Compare the two images that are pulled from the s3 bucket
    face_matches=compare_faces(reference, verificationImage)
    return str(face_matches)



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
