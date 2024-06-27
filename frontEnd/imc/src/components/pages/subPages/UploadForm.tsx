import React, { useState } from 'react';
import axios from 'axios';
import { Form, Container, Row, Col } from 'react-bootstrap';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './UploadForm.css'; // Import custom CSS

const UploadForm = () => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setFile(event.target.files ? event.target.files[0] : null);
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!file) {
      toast.error("Please select a file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);

    try {
      const response = await axios.post('http://localhost:8000/api/upload-quote/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.status === 'success') {
        toast.success('File uploaded and processed successfully.');
      } else {
        toast.error('An error occurred while processing the file.');
      }
    } catch (err) {
      toast.error('An error occurred while uploading the file.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container>
      <ToastContainer />
      <Row className="justify-content-md-center">
        <Col md="8">
          <h2 className="text-center my-4">Upload Quote File</h2>
          <Form onSubmit={handleSubmit} className="p-4 border rounded shadow-sm">
            <Form.Group controlId="formFile" className="mb-3">
              <Form.Label className="file-upload-label">Select file to upload</Form.Label>
              <div className="file-input-container">
                <div className={`custom-file ${file ? 'file-selected' : 'file-not-selected'}`}>
                  <input type="file" className="custom-file-input" onChange={handleFileChange} />
                  <label className="custom-file-label">{file ? file.name : "Choose file"}</label>
                </div>
                {file && (
                  <button 
                    type="submit" 
                    disabled={loading} 
                    className={`upload-button ${loading ? 'loading' : ''}`}
                  >
                    {loading ? "Loading..." : "Upload"}
                  </button>
                )}
              </div>
            </Form.Group>
          </Form>
        </Col>
      </Row>
    </Container>
  );
};

export default UploadForm;
