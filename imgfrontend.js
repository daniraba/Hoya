import React, { useState } from "react";

const OCRUploader = () => {
  const [file, setFile] = useState(null);
  const [text, setText] = useState("");

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

    try {
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (response.ok) {
        setText(data.extracted_text);
      } else {
        alert(data.error || "Failed to upload image!");
      }
    } catch (err) {
      alert("Error uploading file!");
    }
  };

  return (
    <div className="app">
      <h1>OCR Uploader</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      {text && (
        <div>
          <h2>Extracted Text:</h2>
          <pre>{text}</pre>
        </div>
      )}
    </div>
  );
};

export default OCRUploader;
