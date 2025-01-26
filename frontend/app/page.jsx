'use client'

// import SessionCard from "@components/SessionCard";
// import Feed from "@components/Feed";
// import ReactGrid from "@components/ReactGrid";
// import { useSession } from "next-auth/react";

import { useRouter } from "@node_modules/next/navigation";
import { useState, useEffect, useRef } from "react";
import { useToast } from "@hooks/use-toast";
export default function Home() {

  const router = useRouter()

  const storyRef = useRef(null);

  const scrollToStory = () => {
    storyRef.current.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <>
    <section className="w-2/3 flex-center flex-col mb-16 mt-8">
    <h1 className="head_text text-center black_gradient py-2 ">
      Prevent Misdiagnosis of Diabetes
    </h1>
    <br/>
    <p className="desc text-center">
      Medicare is a website created aiming to reduce the number of misdiagnosis of Type 1 diabetes over Type 2 diabetes. 
    </p>
    <div className="flex-center gap-4 mt-8">
      <button className="black_btn" onClick={() => router.push('/trial')}>
        Jump to Diagnostic Tool
      </button>
      <button className="outline_btn" onClick={scrollToStory}>
        Learn More
      </button>
    </div>
    </section>


    <div className="mt-44 w-4/5" ref={storyRef}>
      <h1 className="text-5xl font-bold black_gradient flex-start py-12">
        Our Story
      </h1>
      <div className="">
        <h1 className="text-2xl font-bold">
          What inspired Us?
        </h1>
        <p className="mt-4 text-zinc-600">
        According to recent scientific studies, approximately 40% of adults older than 30 years 
        with type 1 diabetes have been misdiagnosed with type 2 diabetes. Diabetes being such a common disease amongst the elderly, this significant 
        misdiagnosis rate can lead to serious consequences due to the difference in appropriate 
        treatment. After learning this alarming statistic, we set out to create a tool that could 
        help reduce the rate of these errors and ensure patients receive the proper care they 
        need.
        </p>
      </div>
      <div className="mt-8">
        <h1 className="text-2xl font-bold">
          So, what did we do?
        </h1>
        <p className="mt-4 text-zinc-600">
        BetterSteps simplifies the process of identifying diabetes type by analyzing lab reports. 
        Users can upload an image of a lab report, which our platform processes to extract and 
        classify relevant data. Key indicators such as BMI, insulin levels, skin thickness, diabetes 
        pedigree, age, blood pressure, and glucose are used to predict the type of diabetes. If the 
        image processing encounters issues, users can manually input the details.
        </p>
      </div>
      <div className="mt-8">
        <h1 className="text-2xl font-bold">
          How did we build it?
        </h1>
        <p className="mt-4 text-zinc-600">
        Our solution is powered by a machine learning model built using a dataset from Kaggle. 
        The model uses Random Forest Trees classification to make predictions. On the front end, 
        we designed an interface that accepts both image uploads and manual inputs. For the 
        backend, we used Django and Flask to process the data. We also integrated Tesseract OCR 
        to extract text from images, allowing for data interpretation from lab reports.
        </p>
      </div>
      <div className="mt-8">
        <h1 className="text-2xl font-bold">
          What's next for us?
        </h1>
        <p className="mt-4 text-zinc-600">
        Our vision is to make BetterSteps widely accessible to the public. By gathering user feedback, we aim to refine our model and enhance its accuracy and usability. Ultimately, we hope to contribute to better health outcomes by empowering individuals and healthcare providers with a reliable tool to aid in diabetes diagnosis.
        </p>
      </div>

    </div>
    
    </>

  );
}