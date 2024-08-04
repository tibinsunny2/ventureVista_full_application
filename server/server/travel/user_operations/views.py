import random
import string
from django.utils import timezone
from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import CustomUser,Package,Comments,Blogs
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import RetrieveAPIView,UpdateAPIView
from django.core.mail import send_mail



class UserloginView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer
    

class AdminloginView(TokenObtainPairView):
    serializer_class = AdminTokenObtainPairSerializer
    


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    serializer_class=CustomUserSerializer
    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully",'data':serializer.data},status=status.HTTP_201_CREATED)
        return Response({"message": "User registration failed", "errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SuperuserRegistrationView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            # Set is_superuser to True for superuser registration
            serializer.validated_data['is_superuser'] = True
            serializer.save()
            return Response({"message": "User registered successfully", 'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response({"message": "User registration failed", "errors": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

class UserDetailsView(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class UpdateUserDetailsView(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserupdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user







class PackageCRUDView(APIView):
    serializer_class = PackageSerializer
    def post(self, request):
        serializer = PackageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['admin'] = self.request.user
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        package = Package.objects.get(pk=pk)
        serializer = PackageSerializer(package, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        package = Package.objects.get(pk=pk)
        serializer = PackageSerializer(package, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            package = Package.objects.get(pk=pk)
            package.delete()
            return Response({'detail': 'Package deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Package.DoesNotExist:
            return Response({'detail': 'Package not found.'}, status=status.HTTP_404_NOT_FOUND)



class ListPackagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            packages = Package.objects.all()
            serializer = PackageSerializer(packages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Packages not found.'}, status=status.HTTP_404_NOT_FOUND)


class PackageSelectionGet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request,pk):
        try:
            packages = PackageSelection.objects.get(id=pk)
            print(packages)
            serializer = PackageSelectionSerializer(packages)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Selection Package not found.'}, status=status.HTTP_404_NOT_FOUND)

class PackageDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            package = Package.objects.get(pk=pk)
            serializer = PackageSerializer(package)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Package.DoesNotExist:
            return Response({'detail': 'Package not found.'}, status=status.HTTP_404_NOT_FOUND)

class PackageSelectionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            try:
                package = Package.objects.get(pk=pk)
                print(package)
            except Package.DoesNotExist:
                return Response({'detail': 'Package not found.'}, status=status.HTTP_404_NOT_FOUND)
            people=request.data.get('no_of_people')
            print(people)
            amount = int(package.amount) * int(people)
            selection, created = PackageSelection.objects.get_or_create(user=request.user, package=package,no_of_people=people,amount=amount)
            ser=PackageSelectionSerializer(selection)
            return Response({'detail': 'Package selected successfully.','data':ser.data}, status=status.HTTP_201_CREATED)
        except:
            return Response({'detail': 'Package Not Selected.'}, status=status.HTTP_400_BAD_REQUEST)



class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            packageselected = PackageSelection.objects.get(pk=pk)
            print(packageselected)
        except PackageSelection.DoesNotExist:
            return Response({'detail': 'Selected Package not found.'}, status=status.HTTP_404_NOT_FOUND)
        card=request.data.get('card_number')
        name=request.data.get('cardholder')
        cvv=request.data.get('cvv')
        exp=request.data.get('exp')
        selection, created = UserPayment.objects.get_or_create(user=request.user, package=packageselected,card_number=card,cardholder=name,cvv=cvv,exp=exp)
        if created:
            ser=PaymentSerializer(selection)
            return Response({'detail': 'Payment  successfull.','data':ser.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'Payment unsuccessfull'}, status=status.HTTP_400_BAD_REQUEST)





class AdminPackageSelectionListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        selections = PackageSelection.objects.all()
        serializer = PackageSelectionSerializer(selections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            package = Package.objects.get(pk=pk)
            serializer = CommentSerializer(data=request.data)

            if serializer.is_valid():
                serializer.validated_data['user'] = self.request.user
                serializer.validated_data['package'] = package
                serializer.save()
                return Response({"message": "Comment created successfully",'data':serializer.data}, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Package.DoesNotExist:
            return Response({'detail': 'Package not found.'}, status=status.HTTP_404_NOT_FOUND)

class ListCommentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            package = Package.objects.get(pk=pk)
            comments = Comments.objects.filter(package=package)
            serializer = CommentlistSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


        except Package.DoesNotExist:
            return Response({'detail': 'Package not found.'}, status=status.HTTP_404_NOT_FOUND)


class DeleteCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            comment = Comments.objects.get(pk=pk, user=request.user)
            comment.delete()
            return Response({'detail': 'Comment deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

        except Comments.DoesNotExist:
            return Response({'detail': 'Comment not found or you do not have permission to delete it.'}, status=status.HTTP_404_NOT_FOUND)



class CreateBlogView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = BlogSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['user'] = self.request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListBlogsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            blogs = Blogs.objects.all()
            serializer = BloglistSerializer(blogs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Blogs.DoesNotExist:
            return Response({'detail': 'Blogs not found.'}, status=status.HTTP_404_NOT_FOUND)

class BlogDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            blog = Blogs.objects.get(pk=pk)
            serializer = BlogSerializer(blog)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Blogs.DoesNotExist:
            return Response({'detail': 'Blog not found.'}, status=status.HTTP_404_NOT_FOUND)



class ListUserBlogsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_blogs = Blogs.objects.filter(user=request.user)
            serializer = BloglistSerializer(user_blogs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Blogs.DoesNotExist:
            return Response({'detail': 'Blogs not found.'}, status=status.HTTP_404_NOT_FOUND)


class UpdateBlogView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            blog = Blogs.objects.get(pk=pk, user=self.request.user)
            serializer = BlogSerializer(blog, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Blogs.DoesNotExist:
            return Response({'detail': 'Blog not found or you do not have permission to update it.'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            blog = Blogs.objects.get(pk=pk, user=self.request.user)
            serializer = BlogSerializer(blog, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Blogs.DoesNotExist:
            return Response({'detail': 'Blog not found or you do not have permission to update it.'}, status=status.HTTP_404_NOT_FOUND)


class DeleteBlogView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            blog = Blogs.objects.get(pk=pk, user=self.request.user)
            blog.delete()
            return Response({'detail': 'Blog deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

        except Blogs.DoesNotExist:
            return Response({'detail': 'Blog not found or you do not have permission to delete it.'}, status=status.HTTP_404_NOT_FOUND)
        




class CreatReviewView(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    def post(self, request):

        serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid():
            # serializer.validated_data['user'] = self.request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListReviewView(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ReviewlistSerializer
    def get(self, request):
        try:
            reviews = Review.objects.all()
            serializer = ReviewlistSerializer(reviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Blogs.DoesNotExist:
            return Response({'detail': 'review not found.'}, status=status.HTTP_404_NOT_FOUND)

class ReviewDetailView(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    def get(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Blogs.DoesNotExist:
            return Response({'detail': 'review not found.'}, status=status.HTTP_404_NOT_FOUND)



        


class PasswordResetOTPSendView(APIView):
    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response({'error': 'email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'No user with this email'}, status=status.HTTP_404_NOT_FOUND)

        # Generate a random 6-character OTP
        otp = ''.join(random.choices(string.digits, k=6))

        # Store OTP and timestamp in the session
        request.session['otp'] = otp
        request.session['otp_timestamp'] = timezone.now().timestamp()
        request.session['email'] = email

        # Send the OTP to the user's email
        subject = 'Password Reset OTP'
        message = f'Your OTP for password reset is: {otp}.valid upto 5 minutes'
        from_email = 'jipsongeorge753@gmail.com'
        to_email = email
        send_mail(subject, message, from_email, [to_email], fail_silently=False)

        return Response({'detail': 'OTP sent to your email'}, status=status.HTTP_200_OK)
    

class OTPValidationView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email or not otp:
            return Response({'error': 'email and otp are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve OTP and timestamp from the session
        stored_otp = request.session.get('otp')
        stored_email = request.session.get('email')
        timestamp = request.session.get('otp_timestamp')

        # Verify the OTP
        if stored_otp == otp and timezone.now().timestamp() - timestamp <= 300 and stored_email == email:
            # OTP is valid and not expired (within 5 minutes)
            # You can add additional logic here if needed
            return Response({'detail': 'OTP validation successful'}, status=status.HTTP_200_OK)
        
        elif timezone.now().timestamp() - timestamp >= 300 :
            request.session.pop('otp', None)
            request.session.pop('otp_timestamp', None)
            request.session.pop('email', None)
            return Response({'detail': 'expired OTP'}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            # Clear the session data if OTP is invalid or expired

            return Response({'detail': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        
class ChangePasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp=request.data.get('otp')
        new_password = request.data.get('new_password')

        if not email or not new_password or not otp:
            return Response({'error': 'email and new_password or otp are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        stored_otp = request.session.get('otp')
        stored_email = request.session.get('email')
        timestamp = request.session.get('otp_timestamp')
        
        if stored_otp == otp and stored_email == email:
        
            user = CustomUser.objects.get(email=email)
            if user is None:
                return Response({'detail': 'Invalid user or password'}, status=status.HTTP_401_UNAUTHORIZED)

        # Change the user's password
            user.set_password(new_password)
            user.save()

        # Clear the session data after successful password change
            request.session.pop('otp', None)
            request.session.pop('otp_timestamp', None)
            request.session.pop('email', None)

            return Response({'detail': 'Password changed successfully'}, status=status.HTTP_200_OK)
            
        else:
            return Response({'detail': 'Invalid email or OTP'}, status=status.HTTP_400_BAD_REQUEST)