from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import HttpResponseBadRequest
import random
from rest_framework import status, serializers
from rest_framework.response import Response


def confirm_email(request):
    if request.method == 'POST':
        class ConfirmationSerializer(serializers.Serializer):
            confirmation_code = serializers.CharField()

        if 'email' not in request.data:
            return HttpResponseBadRequest('Email field is missing')

        user_email = request.data.get('email')
        confirmation_code = random.randint(10000, 99999)

        subject = 'Email Confirmation'
        from_email = 'your@example.com'  # Replace with your email address or use a proper email sender
        to_email = [user_email]

        # HTML content of the email
        html_content = f'''
                    <html>
                    <head>
                        <style>
                            .code {{
                                font-size: 24px;
                            }}
                        </style>
                    </head>
                    <body>
                        <p>Your confirmation code is:</p>
                        <p class="code">{confirmation_code}</p>
                        <p>Please enter this code to verify your email address and complete the registration process.</p>
                        <p>If you did not request this confirmation, please disregard this email.</p>
                        <p>Kind regards,</p>
                        <p>The ShipperAuto Team</p>
                    </body>
                    </html>
                '''

        try:
            # Send email
            email_message = EmailMultiAlternatives(subject, '', from_email, to_email)
            email_message.attach_alternative(html_content, 'text/html')
            email_message.send()
            serializer = ConfirmationSerializer({'confirmation_code': confirmation_code})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return HttpResponseBadRequest('Failed to send email')

    return HttpResponseBadRequest('Invalid request method')
