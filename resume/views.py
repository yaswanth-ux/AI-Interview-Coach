from rest_framework.views import APIView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .utils import extract_resume_data
from .models import Resume
from .serializers import ResumeSerializer
from PyPDF2 import PdfReader

class ResumeUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ResumeSerializer(data=request.data)
        if serializer.is_valid():
            resume = serializer.save(user=request.user)

            # Parse PDF and extract text
            pdf_reader = PdfReader(resume.file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""

            resume.extracted_text = text
            resume.save()

            return Response(ResumeSerializer(resume).data)
        return Response(serializer.errors, status=400)


class ResumeParsedDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            latest_resume = Resume.objects.filter(user=request.user).latest('uploaded_at')
            extracted = extract_resume_data(latest_resume.extracted_text)
            return Response(extracted)
        except Resume.DoesNotExist:
            return Response({"error": "No resume found."}, status=404)
        

@login_required
def resume_upload_html(request):
    message = ""
    uploaded = False
    parsed_data = None

    # ✅ Capture round and job_role from query params
    round_type = request.GET.get("round", "Technical")
    job_role = request.GET.get("job_role", "Software Developer")

    if request.method == "POST" and request.FILES.get("resume"):
        uploaded_file = request.FILES["resume"]
        resume = Resume.objects.create(user=request.user, file=uploaded_file)

        # Extract text from PDF
        text = ""
        pdf_reader = PdfReader(resume.file)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""

        resume.extracted_text = text
        resume.save()

        # Parse resume text
        parsed_data = extract_resume_data(text)

        message = "Resume uploaded successfully!"
        uploaded = True

    return render(request, "resume_upload.html", {
        "message": message,
        "uploaded": uploaded,
        "parsed_data": parsed_data,
        "round_type": round_type,         # ✅ Pass to template
        "job_role": job_role          # ✅ Pass to template
    })
