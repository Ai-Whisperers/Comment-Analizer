import React, { useState, useCallback, useEffect } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Button,
  Card,
  CardContent,
  LinearProgress,
  Alert,
  Chip,
  Divider,
  CircularProgress
} from '@mui/material';
import {
  CloudUpload,
  Analytics,
  Download,
  CheckCircle,
  Error as ErrorIcon,
  Refresh
} from '@mui/icons-material';
import { styled } from '@mui/material/styles';
import { motion } from 'framer-motion';
import { useDropzone } from 'react-dropzone';
import toast from 'react-hot-toast';

// Import our API and types
import {
  uploadFile,
  startAnalysis,
  getAnalysisStatus,
  getAnalysisResults,
  exportResults
} from '../services/api';
import type { 
  AnalysisResults, 
  FileUploadResponse, 
  AnalysisJobResponse 
} from '../types/analysis';
import { errorHandler } from '../services/error-handler';

// Styled components
const DropZone = styled(Paper, {
  shouldForwardProp: (prop) => prop !== 'isDragActive'
})<{ isDragActive?: boolean }>(({ theme, isDragActive }) => ({
  border: `2px dashed ${isDragActive ? theme.palette.primary.main : theme.palette.grey[300]}`,
  borderRadius: theme.shape.borderRadius,
  padding: theme.spacing(4),
  textAlign: 'center',
  cursor: 'pointer',
  transition: 'border-color 0.3s ease',
  backgroundColor: isDragActive ? theme.palette.action.hover : 'transparent',
  '&:hover': {
    borderColor: theme.palette.primary.main,
    backgroundColor: theme.palette.action.hover,
  }
}));

const StatsCard = styled(Card)(({ theme }) => ({
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  transition: 'transform 0.2s',
  '&:hover': {
    transform: 'translateY(-4px)',
  }
}));

interface UnifiedDashboardProps {}

const UnifiedDashboard: React.FC<UnifiedDashboardProps> = () => {
  // State
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [fileId, setFileId] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisProgress, setAnalysisProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState('');
  const [jobId, setJobId] = useState<string | null>(null);
  const [results, setResults] = useState<AnalysisResults | null>(null);
  const [error, setError] = useState<string | null>(null);

  // File upload with drag & drop
  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    // Validate file
    if (file.size > 50 * 1024 * 1024) {
      errorHandler.handleFileError('File size exceeds 50MB limit', file.name);
      return;
    }

    const allowedTypes = ['.xlsx', '.xls', '.csv', '.json', '.txt'];
    const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();
    
    if (!allowedTypes.includes(fileExtension)) {
      errorHandler.handleFileError('Unsupported file type. Please use Excel, CSV, JSON, or TXT files.', file.name);
      return;
    }

    setUploadedFile(file);
    setError(null);
    await uploadFileToServer(file);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls'],
      'application/json': ['.json'],
      'text/plain': ['.txt']
    },
    multiple: false
  });

  const uploadFileToServer = async (file: File) => {
    setIsUploading(true);
    try {
      const response = await uploadFile(file);
      setFileId(response.file_id);
      toast.success('File uploaded successfully!');
    } catch (error) {
      const errorMessage = errorHandler.handleAPIError(error as Error);
      setError(errorMessage);
    } finally {
      setIsUploading(false);
    }
  };

  const startAnalysisProcess = async () => {
    if (!fileId) {
      toast.error('Please upload a file first');
      return;
    }

    setIsAnalyzing(true);
    setAnalysisProgress(0);
    setCurrentStep('Starting analysis...');
    setError(null);

    try {
      // Start analysis with multiple analysis types
      const analysisResponse = await startAnalysis(fileId, [
        'sentiment',
        'emotion', 
        'theme',
        'nps',
        'churn'
      ]);
      
      setJobId(analysisResponse.job_id);
      
      // Start polling for progress
      pollAnalysisProgress(analysisResponse.job_id);
      
    } catch (error) {
      const errorMessage = errorHandler.handleAPIError(error as Error);
      setError(errorMessage);
      setIsAnalyzing(false);
    }
  };

  const pollAnalysisProgress = async (jobId: string) => {
    const pollInterval = setInterval(async () => {
      try {
        const status = await getAnalysisStatus(jobId);
        
        setAnalysisProgress(status.progress || 0);
        setCurrentStep(status.current_step || 'Processing...');
        
        if (status.status === 'completed') {
          clearInterval(pollInterval);
          const results = await getAnalysisResults(jobId);
          setResults(results);
          setIsAnalyzing(false);
          toast.success('Analysis completed successfully!');
        } else if (status.status === 'failed') {
          clearInterval(pollInterval);
          setError(status.message || 'Analysis failed');
          setIsAnalyzing(false);
        }
      } catch (error) {
        clearInterval(pollInterval);
        const errorMessage = errorHandler.handleAPIError(error as Error);
        setError(errorMessage);
        setIsAnalyzing(false);
      }
    }, 2000);

    // Cleanup after 5 minutes
    setTimeout(() => {
      clearInterval(pollInterval);
      if (isAnalyzing) {
        setError('Analysis timeout - please try again');
        setIsAnalyzing(false);
      }
    }, 5 * 60 * 1000);
  };

  const downloadResults = async () => {
    if (!jobId || !results) {
      toast.error('No results to download');
      return;
    }

    try {
      const blob = await exportResults(jobId, 'json');
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'analysis_results.json';
      link.click();
      URL.revokeObjectURL(url);
      toast.success('Results downloaded successfully!');
    } catch (error) {
      errorHandler.handleAPIError(error as Error);
    }
  };

  const resetDashboard = () => {
    setUploadedFile(null);
    setFileId(null);
    setJobId(null);
    setResults(null);
    setError(null);
    setIsAnalyzing(false);
    setAnalysisProgress(0);
    setCurrentStep('');
  };

  return (
    <Box sx={{ p: 3 }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Typography variant="h4" gutterBottom sx={{ textAlign: 'center', mb: 4 }}>
          Comment Analysis Dashboard
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
            {error}
          </Alert>
        )}

        <Grid container spacing={3}>
          {/* File Upload Section */}
          <Grid item xs={12} lg={6}>
            <Paper sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                <CloudUpload sx={{ mr: 1, verticalAlign: 'middle' }} />
                Data Upload
              </Typography>
              
              <DropZone {...getRootProps()} isDragActive={isDragActive}>
                <input {...getInputProps()} />
                
                {isUploading ? (
                  <Box>
                    <CircularProgress sx={{ mb: 2 }} />
                    <Typography>Uploading file...</Typography>
                  </Box>
                ) : uploadedFile ? (
                  <Box>
                    <CheckCircle sx={{ fontSize: 48, color: 'success.main', mb: 2 }} />
                    <Typography variant="h6">{uploadedFile.name}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB
                    </Typography>
                    <Chip 
                      label="Ready for analysis" 
                      color="success" 
                      sx={{ mt: 1 }}
                    />
                  </Box>
                ) : (
                  <Box>
                    <CloudUpload sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                    <Typography variant="h6">
                      {isDragActive ? 'Drop file here...' : 'Drag & drop file or click to browse'}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Supports CSV, Excel, JSON, and TXT files (max 50MB)
                    </Typography>
                  </Box>
                )}
              </DropZone>

              <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
                <Button
                  variant="contained"
                  startIcon={<Analytics />}
                  onClick={startAnalysisProcess}
                  disabled={!fileId || isAnalyzing || isUploading}
                  fullWidth
                >
                  {isAnalyzing ? 'Analyzing...' : 'Start Analysis'}
                </Button>
                
                <Button
                  variant="outlined"
                  startIcon={<Refresh />}
                  onClick={resetDashboard}
                  disabled={isAnalyzing || isUploading}
                >
                  Reset
                </Button>
              </Box>
            </Paper>
          </Grid>

          {/* Analysis Progress */}
          <Grid item xs={12} lg={6}>
            <Paper sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                Analysis Progress
              </Typography>
              
              {isAnalyzing ? (
                <Box>
                  <LinearProgress 
                    variant="determinate" 
                    value={analysisProgress} 
                    sx={{ mb: 2 }}
                  />
                  <Typography variant="body2" color="text.secondary">
                    {analysisProgress}% - {currentStep}
                  </Typography>
                </Box>
              ) : results ? (
                <Box>
                  <Alert severity="success" sx={{ mb: 2 }}>
                    Analysis completed successfully!
                  </Alert>
                  <Button
                    variant="contained"
                    startIcon={<Download />}
                    onClick={downloadResults}
                    fullWidth
                    color="success"
                  >
                    Download Results
                  </Button>
                </Box>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  Upload a file to start analysis
                </Typography>
              )}
            </Paper>
          </Grid>

          {/* Results Display */}
          {results && (
            <>
              <Grid item xs={12}>
                <Divider sx={{ my: 2 }}>
                  <Typography variant="h6">Analysis Results</Typography>
                </Divider>
              </Grid>

              {/* Sentiment Analysis */}
              <Grid item xs={12} md={6} lg={3}>
                <StatsCard>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Sentiment Analysis
                    </Typography>
                    {results.sentiment_analysis ? (
                      <Box>
                        <Typography variant="body2">
                          Positive: {results.sentiment_analysis.positive?.toFixed(1)}%
                        </Typography>
                        <Typography variant="body2">
                          Negative: {results.sentiment_analysis.negative?.toFixed(1)}%
                        </Typography>
                        <Typography variant="body2">
                          Neutral: {results.sentiment_analysis.neutral?.toFixed(1)}%
                        </Typography>
                      </Box>
                    ) : (
                      <Typography variant="body2" color="text.secondary">
                        No data available
                      </Typography>
                    )}
                  </CardContent>
                </StatsCard>
              </Grid>

              {/* Emotion Analysis */}
              <Grid item xs={12} md={6} lg={3}>
                <StatsCard>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Emotion Analysis
                    </Typography>
                    {results.emotion_analysis ? (
                      <Box>
                        {Object.entries(results.emotion_analysis).map(([emotion, value]) => (
                          <Typography key={emotion} variant="body2">
                            {emotion}: {typeof value === 'number' ? value.toFixed(1) : value}%
                          </Typography>
                        ))}
                      </Box>
                    ) : (
                      <Typography variant="body2" color="text.secondary">
                        No data available
                      </Typography>
                    )}
                  </CardContent>
                </StatsCard>
              </Grid>

              {/* NPS Scores */}
              <Grid item xs={12} md={6} lg={3}>
                <StatsCard>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      NPS Scores
                    </Typography>
                    {results.nps_analysis ? (
                      <Box>
                        <Typography variant="body2" sx={{ color: 'success.main' }}>
                          Promoters: {results.nps_analysis.promoters?.toFixed(1)}%
                        </Typography>
                        <Typography variant="body2" sx={{ color: 'warning.main' }}>
                          Passives: {results.nps_analysis.passives?.toFixed(1)}%
                        </Typography>
                        <Typography variant="body2" sx={{ color: 'error.main' }}>
                          Detractors: {results.nps_analysis.detractors?.toFixed(1)}%
                        </Typography>
                      </Box>
                    ) : (
                      <Typography variant="body2" color="text.secondary">
                        No data available
                      </Typography>
                    )}
                  </CardContent>
                </StatsCard>
              </Grid>

              {/* Churn Risk */}
              <Grid item xs={12} md={6} lg={3}>
                <StatsCard>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Churn Risk
                    </Typography>
                    {results.churn_analysis ? (
                      <Box>
                        <Typography variant="body2" sx={{ color: 'error.main' }}>
                          High Risk: {results.churn_analysis.high_risk?.toFixed(1)}%
                        </Typography>
                        <Typography variant="body2" sx={{ color: 'warning.main' }}>
                          Medium Risk: {results.churn_analysis.medium_risk?.toFixed(1)}%
                        </Typography>
                        <Typography variant="body2" sx={{ color: 'success.main' }}>
                          Low Risk: {results.churn_analysis.low_risk?.toFixed(1)}%
                        </Typography>
                      </Box>
                    ) : (
                      <Typography variant="body2" color="text.secondary">
                        No data available
                      </Typography>
                    )}
                  </CardContent>
                </StatsCard>
              </Grid>

              {/* Recommendations */}
              {results.recommendations && results.recommendations.length > 0 && (
                <Grid item xs={12}>
                  <Paper sx={{ p: 3 }}>
                    <Typography variant="h6" gutterBottom>
                      Recommendations
                    </Typography>
                    {results.recommendations.map((recommendation, index) => (
                      <Alert key={index} severity="info" sx={{ mb: 1 }}>
                        {recommendation}
                      </Alert>
                    ))}
                  </Paper>
                </Grid>
              )}
            </>
          )}
        </Grid>
      </motion.div>
    </Box>
  );
};

export default UnifiedDashboard;