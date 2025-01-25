import React, { useState } from "react";

const OCRUploader = () => {
  const [file, setFile] = useState(null);
  const [text, setText] = useState("");
  const [diabetesType, setDiabetesType] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setIsLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (response.ok) {
        setText(data.ocr_text || "No text extracted");
        setDiabetesType(data.diabetes_type || "No prediction made");
      } else {
        alert(data.error || "Failed to process image!");
      }
    } catch (err) {
      alert("Error connecting to the server!");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      <h1>OCR Uploader</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={isLoading}>
        {isLoading ? "Uploading..." : "Upload"}
      </button>
      {text && (
        <div>
          <h2>Extracted Text:</h2>
          <pre>{text}</pre>
        </div>
      )}
      {diabetesType && (
        <div>
          <h2>Predicted Diabetes Type:</h2>
          <p>{diabetesType}</p>
        </div>
      )}
    </div>
  );
};

export default OCRUploader;
