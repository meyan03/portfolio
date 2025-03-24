import logging

from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.db.models import Avg, Sum, Count
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User, Product, Invoice, Cart, CartItem
from .serializers import MyTokenObtainPairSerializer
from .serializers import UserSerializer, ProductSerializer, InvoiceSerializer
from .utils import fetch_product_from_open_food_facts

logger = logging.getLogger(__name__)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        logger.info(f"Login attempt: {request.data}")
        return super().post(request, *args, **kwargs)


# ViewSet pour les utilisateurs
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin

class ProductViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'barcode'

    def list(self, request):
        """
        GET: Retrieve all products
        """
        products = Product.objects.all()
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, barcode=None):
        """
        GET: Retrieve a product by barcode
        """
        product = get_object_or_404(Product, barcode=barcode)
        serializer = self.get_serializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        POST: Create a new product
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, barcode=None):
        """
        PUT: Update an existing product by barcode
        """
        product = get_object_or_404(Product, barcode=barcode)
        serializer = self.get_serializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, barcode=None):
        """
        DELETE: Remove a product by barcode
        """
        product = get_object_or_404(Product, barcode=barcode)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class UserRoleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "is_admin": request.user.is_admin,
            "is_staff": request.user.is_staff,
            "is_superuser": request.user.is_superuser
        }, status=200)



class KPIView(APIView):
    def get(self, request):
        try:
            # Calcul des KPI
            average_purchase = Invoice.objects.aggregate(average=Avg('total'))['average']
            total_sales = Invoice.objects.aggregate(total=Sum('total'))['total']
            active_customers = Invoice.objects.values('user').distinct().count()
            total_customers = User.objects.filter(is_active=True).count()
            most_purchased_products = Product.objects.annotate(num_invoices=Count('invoice')).order_by('-num_invoices')[:5]
            median_payment = Invoice.objects.aggregate(median=Avg('total'))['median']

            # Nouveaux KPIs
            total_stock = Product.objects.aggregate(total_stock=Sum('available_quantity'))['total_stock'] or 0
            cart_usage = Cart.objects.filter(products__isnull=False).count()
            cart_usage_rate = (cart_usage / total_customers) * 100 if total_customers > 0 else 0

            # Structurer les données
            data = {
                "average_purchase": average_purchase,
                "total_sales": total_sales,
                "active_customers": active_customers,
                "total_customers": total_customers,
                "most_purchased_products": [
                    {"name": p.name, "num_invoices": p.num_invoices} for p in most_purchased_products
                ],
                "median_payment": median_payment,
                "total_stock": total_stock,
                "cart_usage_rate": cart_usage_rate,
            }

            return Response(data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class InvoiceViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing invoices.
    """
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        GET: Retrieve all invoices
        """
        invoices = Invoice.objects.all()
        serializer = self.get_serializer(invoices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        GET: Retrieve a single invoice by ID
        """
        invoice = get_object_or_404(Invoice, pk=pk)
        serializer = self.get_serializer(invoice)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        POST: Create a new invoice
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        PUT: Update an existing invoice
        """
        invoice = get_object_or_404(Invoice, pk=pk)
        serializer = self.get_serializer(invoice, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        DELETE: Delete an invoice
        """
        invoice = get_object_or_404(Invoice, pk=pk)
        invoice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            logger.error("Email ou mot de passe manquant.")
            return Response({"error": "Email et mot de passe sont requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            logger.error(f"Utilisateur avec l'email {email} introuvable.")
            return Response({"error": "Email ou mot de passe incorrect."}, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(username=user.username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        else:
            logger.error("Mot de passe incorrect.")
            return Response({"error": "Email ou mot de passe incorrect."}, status=status.HTTP_401_UNAUTHORIZED)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = request.data

            # Required fields check
            required_fields = ['username', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'billing_address']
            for field in required_fields:
                if field not in data or not data[field]:
                    return Response({"error": f"The field {field} is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the email is already in use
            if User.objects.filter(email=data['email']).exists():
                return Response({"error": "This email is already in use."}, status=status.HTTP_400_BAD_REQUEST)

            # Create the user
            user = User.objects.create(
                username=data['username'],
                email=data['email'],
                password=make_password(data['password']),
                first_name=data['first_name'],
                last_name=data['last_name'],
                phone_number=data['phone_number'],
                billing_address=data['billing_address'],
            )
            return Response({"message": "User successfully created."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Internal server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

logger = logging.getLogger(__name__)

class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]  # L'utilisateur doit être authentifié

    def get(self, request):
        """
        Récupère les produits du panier de l'utilisateur.
        """
        try:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
            data = [
                {
                    "id": item.id,
                    "product_id": item.product.id,
                    "product_name": item.product.name,
                    "price": item.product.price,
                    "quantity": item.quantity,
                }
                for item in cart_items
            ]
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du panier : {str(e)}")
            return Response({"error": "Erreur lors de la récupération du panier."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            logger.info(f"Requête reçue : {request.data}")  # Log de la requête
            cart, _ = Cart.objects.get_or_create(user=request.user)
            product_id = request.data.get("product_id")
            quantity = int(request.data.get("quantity", 1))

            if not product_id:
                logger.error("ID du produit manquant.")
                return Response({"error": "ID du produit requis."}, status=status.HTTP_400_BAD_REQUEST)

            product = Product.objects.get(id=product_id)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.save()

            logger.info(f"Produit ajouté au panier : {product.name}")
            return Response({"message": "Produit ajouté au panier avec succès."}, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            logger.error("Produit introuvable.")
            return Response({"error": "Produit introuvable."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            logger.error("Quantité invalide.")
            return Response({"error": "Quantité invalide."}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            logger.error(f"Erreur d'intégrité : {str(e)}")
            return Response({"error": "Erreur d'intégrité dans la base de données."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"Erreur inattendue : {str(e)}")
            return Response({"error": f"Erreur interne du serveur : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def delete(self, request):
        """
        Supprime un produit du panier.
        """
        try:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            product_id = request.data.get("product_id")

            # Validation
            if not product_id:
                return Response({"error": "ID du produit requis."}, status=status.HTTP_400_BAD_REQUEST)

            # Vérifie que le produit existe dans le panier
            try:
                product = Product.objects.get(id=product_id)
                cart_item = CartItem.objects.get(cart=cart, product=product)
                cart_item.delete()
                return Response({"message": "Produit retiré du panier avec succès."}, status=status.HTTP_200_OK)
            except Product.DoesNotExist:
                return Response({"error": "Produit introuvable."}, status=status.HTTP_404_NOT_FOUND)
            except CartItem.DoesNotExist:
                return Response({"error": "Le produit n'est pas dans le panier."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Erreur interne : {str(e)}")
            return Response({"error": "Erreur interne du serveur."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)