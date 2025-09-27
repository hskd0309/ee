// API client for Smart Campus ERP backend

const API_BASE_URL = import.meta.env.PROD ? 'https://your-backend-url.com' : '';

export interface Student {
  id: string;
  roll_no: string;
  name: string;
  email: string;
  class_name: string;
  department: string;
  data_sharing: boolean;
  bri_score: number;
  attendance: number;
  avg_marks: number;
  gpa: number;
  created_at: string;
  updated_at?: string;
}

export interface Assignment {
  id: string;
  student_id: string;
  subject: string;
  title: string;
  due_date: string;
  status: 'pending' | 'completed';
  is_overdue: boolean;
  submitted_at?: string;
  grade?: number;
  created_at: string;
}

export interface Test {
  id: string;
  student_id: string;
  subject: string;
  test_name: string;
  date: string;
  score: number;
  total: number;
  weightage: number;
  created_at: string;
}

export interface Feedback {
  id: string;
  student_id: string;
  text: string;
  category?: string;
  sentiment: 'positive' | 'neutral' | 'negative';
  sentiment_score: number;
  created_at: string;
}

export interface CounsellingSession {
  id: string;
  student_id: string;
  counsellor_name: string;
  referred_by?: string;
  referred_date?: string;
  session_date: string;
  duration_minutes: number;
  status: 'active' | 'in_progress' | 'closed';
  notes?: string;
  outcome?: string;
  created_at: string;
}

export interface StudentSummary {
  id: string;
  name: string;
  roll_no: string;
  bri_score: number;
  attendance: number;
  avg_marks: number;
  assignments_on_time: number;
  sentiment: string;
  data_sharing: boolean;
  bri_history: Array<{ month: string; score: number }>;
  attendance_data: Array<{ name: string; value: number; fill: string }>;
  subject_marks: Array<{ subject: string; marks: number }>;
}

export interface ClassStats {
  class_name: string;
  total_students: number;
  high_risk_count: number;
  medium_risk_count: number;
  low_risk_count: number;
  avg_bri_score: number;
  avg_attendance: number;
}

class ApiClient {
  private baseURL: string;

  constructor() {
    this.baseURL = API_BASE_URL;
  }

  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  // Student endpoints
  async getStudents(): Promise<Student[]> {
    return this.request<Student[]>('/api/students/');
  }

  async getStudent(id: string): Promise<Student> {
    return this.request<Student>(`/api/students/${id}`);
  }

  async getStudentSummary(id: string): Promise<StudentSummary> {
    return this.request<StudentSummary>(`/api/students/${id}/summary`);
  }

  // Assignment endpoints
  async getStudentAssignments(studentId: string): Promise<Assignment[]> {
    return this.request<Assignment[]>(`/api/assignments/${studentId}`);
  }

  // Test endpoints
  async getStudentTests(studentId: string): Promise<Test[]> {
    return this.request<Test[]>(`/api/tests/${studentId}`);
  }

  // Feedback endpoints
  async getStudentFeedback(studentId: string): Promise<Feedback[]> {
    return this.request<Feedback[]>(`/api/feedback/${studentId}`);
  }

  async createFeedback(feedback: { student_id: string; text: string; category?: string }): Promise<Feedback> {
    return this.request<Feedback>('/api/feedback/', {
      method: 'POST',
      body: JSON.stringify(feedback),
    });
  }

  // Counselling endpoints
  async getStudentCounsellingSessions(studentId: string): Promise<CounsellingSession[]> {
    return this.request<CounsellingSession[]>(`/api/counselling/${studentId}`);
  }

  // Class analytics endpoints
  async getClassStats(className: string): Promise<ClassStats> {
    return this.request<ClassStats>(`/api/classes/${className}/stats`);
  }

  // ML endpoints
  async predictBurnout(data: { attendance: number; gpa: number; sentiment_score: number }) {
    return this.request('/api/ml/predict', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
}

export const apiClient = new ApiClient();