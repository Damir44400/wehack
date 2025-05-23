from typing import List

from src.crm.domain.exceptions import NotFoundException
from src.crm.domain.entities.categories import CategoryEntity
from src.crm.domain.interfaces.daos.categories import (
    ICategoryListByCompanyIdDAO
)
from src.crm.domain.interfaces.daos.companies import ICompanyGetDAO


class CategoryGateway(
    ICategoryListByCompanyIdDAO
):
    ...


class CompanyGateway(
    ICompanyGetDAO
):
    ...


class GetCategoriesListUseCase:
    def __init__(
            self,
            category_gateway: CategoryGateway,
            company_gateway: CompanyGateway
    ):
        self._category_gateway = category_gateway
        self._company_gateway = company_gateway

    async def execute(self, company_id: int) -> List[CategoryEntity]:
        db_company = await self._company_gateway.get_by_id(company_id)
        if not db_company:
            raise NotFoundException("Company not found")
        categories = await self._category_gateway.list_by_company_id(db_company.id)
        return categories
