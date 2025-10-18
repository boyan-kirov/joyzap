"""
Data Transfer Object for Gift operations
"""
from typing import Optional


class GiftBody:
    """DTO for gift creation and updates"""
    
    def __init__(
        self,
        name: str,
        description: str,
        category_id: int,
        price: float,
        image_url: str,
        stock_quantity: int = 0,
        is_active: bool = True,
        **kwargs
    ):
        """
        Initialize GiftBody DTO.
        
        Args:
            name: Gift name
            description: Gift description
            category_id: Category ID
            price: Gift price
            image_url: URL to gift image
            stock_quantity: Available stock (default: 0)
            is_active: Whether gift is active (default: True)
            **kwargs: Additional fields to ignore
        """
        self.name = name
        self.description = description
        self.category_id = category_id
        self.price = price
        self.image_url = image_url
        self.stock_quantity = stock_quantity
        self.is_active = is_active
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "category_id": self.category_id,
            "price": self.price,
            "image_url": self.image_url,
            "stock_quantity": self.stock_quantity,
            "is_active": self.is_active
        }
    
    def __repr__(self):
        return f"GiftBody(name={self.name}, price={self.price}, category_id={self.category_id})"
