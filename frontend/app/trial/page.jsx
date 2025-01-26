'use client'

import Create from "@components/Create"
// import { useSession } from "next-auth/react"
import Prediction from "@components/Prediction"
import { useState } from "react"
import { useRouter } from "next/navigation"
import { useToast } from "@hooks/use-toast"
function CreateSession(){

    // const {data: session} = useSession()
    const {toast} = useToast()
    const [fileName, setFileName] = useState(null)
    const [image, setImage] = useState(null);
    const [isReportCorrect, setReportCorrect] = useState(false)
    const [hasSubmittedReport, setSubmittedReport] = useState(false)
    const [submittedData, setSubmittedData] = useState(false)
    const [analysedType, setAnalysedType] = useState(0)
    const router = useRouter()

    const [isChecked, setChecked] = useState(false)
    const [post, setPost] = useState({
        age: '',
        bloodPressure: '',
        insulinLevel: '',
        BMI: '',
        diabetesPedigreeFunction: '',
        bloodGlucose: '',
        pregnancies: '',
        skinThickness: ''       
    })
    const [isSubmitting, setSubmitting] = useState(false)
    const [newType, setNewType] = useState(0)

    const handleFileChange = (e) => {
        const file = e.target.files[0];

        setFileName(file ? file.name : null);

        if(!file) return;

        setImage(file)
      };

    const handleFormSubmitting = () => {

        const submitInput = async() => {

            setSubmitting(true)
            console.log(post)
            try{
                const response = await fetch('http://127.0.0.1:5000/predict_from_data', {
                    method: 'POST',
                    body: JSON.stringify({
                        age: post.age,
                        bloodPressure: post.bloodPressure,
                        insulinLevel: post.insulinLevel,
                        BMI: post.BMI,
                        diabetesPedigreeFunction: post.diabetesPedigreeFunction,
                        bloodGlucose: post.bloodGlucose,
                        pregnancies: post.pregnancies,
                        skinThickness: post.skinThickness
                    })
                    
                })
                if(response.ok){
                    const data = await response.json()
                    setAnalysedType(data.diabetes_type)
                    setNewType(data.diabetes_type.toString())
                    setSubmittedReport(true)
                }
            }
            catch(err){
                console.log(err)

            }
            finally{
                setSubmitting(false)
            }
        }

        const submitImage = async () => {
            setSubmitting(true);
            try{

                const formData = new FormData();
                formData.append('file', image)

                const response = await fetch('http://127.0.0.1:5000/predict', {
                    method: 'POST',
                    body: formData
                    
                })
                if(response.ok){
                    const data = await response.json()
                    console.log(data)
                    const item = {
                        age: String(data.extracted_features.Age),
                        BMI: data.extracted_features.BMI.toString(),
                        bloodPressure: data.extracted_features.BloodPressure.toString(),
                        diabetesPedigreeFunction: data.extracted_features.DiabetesPedigreeFunction.toString(),
                        bloodGlucose: data.extracted_features.Glucose.toString(),
                        insulinLevel: data.extracted_features.Insulin.toString(),
                        pregnancies: data.extracted_features.Pregnancies.toString(),
                        skinThickness: data.extracted_features.SkinThickness.toString()
                    }
                    console.log(item)
                    setPost(item)
                    setNewType(data.diabetes_type.toString())
                    setAnalysedType(data.diabetes_type)
                    setSubmittedReport(true)
                }
            }
            catch(err){
                console.log(err)

            }
            finally{
                setSubmitting(false)
            }
        }

        if(image){
            submitImage()
        }
        else{
            submitInput()
        }
    }

    const handleDataSubmission = () => {

        const item = {
            age: post.age,
            bloodPressure: post.bloodPressure,
            insulinLevel: post.insulinLevel,
            BMI: post.BMI,
            diabetesPedigreeFunction: post.diabetesPedigreeFunction,
            bloodGlucose: post.bloodGlucose,
            diabetesVersion: newType,
            skinThickness: post.skinThickness
        }

        const submitData = async () => {
            setSubmitting(true)

            try{

                const response = await fetch('http://localhost:3000/api/uploadData', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(item)
                   
                })
                if(response.ok){
                    toast({
                        variant: 'success',
                        title: 'Thank you for you contribution',
                        description: "You have successfully posted your information to our database"
                    })
                    setSubmittedData(true)
                }
            }
            catch(err){
                toast({
                    variant: 'destructive',
                    title: 'Oops, something went wrong',
                    description: "We could not post your data to our database..."
                    
                })
                console.log(err)
            }
            finally{
                setSubmitting(false)
            }
        }
        submitData()
    }
    

    return(
        <>
        {!hasSubmittedReport ? (
        <Create
        type='Fill'
        post={post}
        setPost={setPost}
        submitting = {isSubmitting}
        handleSubmitting={handleFormSubmitting}
        fileName={fileName}
        handleFileChange={handleFileChange}
        />
        
        ) : (
        
        <Prediction
        type={analysedType}
        isReportCorrect={isReportCorrect}
        setReportCorect={setReportCorrect}
        newType={newType}
        setNewType={setNewType}
        handleSubmit={handleDataSubmission}
        submittedData={submittedData}
        isSubmitting={isSubmitting}
        post={post}
        />
        )
        
        }
        </>
    )
}

export default CreateSession