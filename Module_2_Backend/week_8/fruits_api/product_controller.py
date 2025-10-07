# Product Controller - Business Logic Layer
from models import Product
from db import db_session
from datetime import datetime
from sqlalchemy.exc import IntegrityError

class ProductController:
    
    @staticmethod
    def get_all_products(filters=None):
        """Get all products with optional filters"""
        query = db_session.query(Product)
        
        if filters:
            # Apply name filter
            if filters.get('name'):
                query = query.filter(Product.name.ilike(f'%{filters["name"]}%'))
            
            # Apply min_price filter
            if filters.get('min_price'):
                try:
                    min_price = float(filters['min_price'])
                    query = query.filter(Product.price >= min_price)
                except ValueError:
                    pass
            
            # Apply max_price filter
            if filters.get('max_price'):
                try:
                    max_price = float(filters['max_price'])
                    query = query.filter(Product.price <= max_price)
                except ValueError:
                    pass
        
        products = query.all()
        return [ProductController._format_product_basic(product) for product in products]
    
    @staticmethod
    def get_product_by_id(product_id):
        """Get a single product by ID"""
        product = db_session.query(Product).filter(Product.id == product_id).first()
        if not product:
            return None
        return ProductController._format_product_full(product)
    
    @staticmethod
    def create_product(data):
        """Create a new product"""
        # Validate required fields
        required_fields = ['name', 'price', 'quantity', 'entry_date']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        try:
            # Validate data types
            price = float(data['price'])
            quantity = int(data['quantity'])
            
            # Parse entry_date
            try:
                entry_date = datetime.fromisoformat(data['entry_date'])
            except ValueError:
                raise ValueError("Invalid entry_date format, use ISO format (YYYY-MM-DD)")
            
            # Create new product
            new_product = Product(
                name=data['name'],
                price=price,
                quantity=quantity,
                entry_date=entry_date
            )
            
            db_session.add(new_product)
            db_session.commit()
            db_session.refresh(new_product)
            
            return ProductController._format_product_full(new_product)
            
        except ValueError as e:
            raise ValueError(str(e))
        except IntegrityError:
            db_session.rollback()
            raise ValueError("An error occurred while creating the product")
        except Exception as e:
            db_session.rollback()
            raise ValueError(str(e))
    
    @staticmethod
    def update_product(product_id, data):
        """Update an existing product"""
        product = db_session.query(Product).filter(Product.id == product_id).first()
        if not product:
            return None
        
        try:
            # Update fields if provided
            if 'name' in data:
                product.name = data['name']
            
            if 'price' in data:
                product.price = float(data['price'])
            
            if 'quantity' in data:
                product.quantity = int(data['quantity'])
            
            if 'entry_date' in data:
                try:
                    product.entry_date = datetime.fromisoformat(data['entry_date'])
                except ValueError:
                    raise ValueError("Invalid entry_date format, use ISO format (YYYY-MM-DD)")
            
            db_session.commit()
            db_session.refresh(product)
            
            return ProductController._format_product_full(product)
            
        except ValueError as e:
            db_session.rollback()
            raise ValueError(str(e))
        except IntegrityError:
            db_session.rollback()
            raise ValueError("An error occurred while updating the product")
        except Exception as e:
            db_session.rollback()
            raise ValueError(str(e))
    
    @staticmethod
    def delete_product(product_id):
        """Delete a product"""
        product = db_session.query(Product).filter(Product.id == product_id).first()
        if not product:
            return False
        
        try:
            db_session.delete(product)
            db_session.commit()
            return True
            
        except IntegrityError:
            db_session.rollback()
            raise ValueError("Cannot delete product because it is referenced by other records")
        except Exception as e:
            db_session.rollback()
            raise ValueError(str(e))
    
    @staticmethod
    def _format_product_basic(product):
        """Format product for basic listing"""
        return {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": product.quantity,
            "entry_date": product.entry_date.isoformat()
        }
    
    @staticmethod
    def _format_product_full(product):
        """Format product with full details"""
        return {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": product.quantity,
            "entry_date": product.entry_date.isoformat(),
            "created_at": product.created_at.isoformat(),
            "updated_at": product.updated_at.isoformat()
        }