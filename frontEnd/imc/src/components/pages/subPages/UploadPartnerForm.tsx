import React, { useState } from 'react';
import axios from 'axios';
import { Form, Button, Spinner, Container, Row, Col } from 'react-bootstrap';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './UploadForm.css'; // Reusing custom CSS

const UploadPartnerForm = () => {
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
      const response = await axios.post('http://localhost:8000/api/upload-partner/', formData, {
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
        <Col md="6">
          <h2 className="text-center my-4">Upload Partner File</h2>
          <Form onSubmit={handleSubmit} className="p-4 border rounded shadow-sm">
            <Form.Group controlId="formFile" className="mb-3">
              <Form.Label>Select file to upload</Form.Label>
              <div className={`custom-file ${file ? 'file-selected' : 'file-not-selected'}`}>
                <input type="file" className="custom-file-input" onChange={handleFileChange} />
                <label className="custom-file-label">{file ? file.name : "Choose file"}</label>
              </div>
              {file && (
                <Button 
                  variant="primary" 
                  type="submit" 
                  disabled={loading} 
                  className="upload-button"
                >
                  {loading ? <Spinner animation="border" size="sm" /> : "Upload"}
                </Button>
              )}
            </Form.Group>
          </Form>
        </Col>
      </Row>
    </Container>
  );
};

export default UploadPartnerForm;
