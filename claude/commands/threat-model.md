# /threat-model

Generate comprehensive threat models for $ARGUMENT using STRIDE methodology with automated risk assessment, attack surface analysis, and mitigation strategies.

## Context Intelligence

### Architecture Discovery

**Automated System Analysis:**

```bash
# Detect application architecture and components
discover_architecture() {
  echo "🏗️ Discovering application architecture..."
  
  # Analyze project structure
  if [ -f "docker-compose.yml" ]; then
    echo "📦 Docker Compose deployment detected"
    DEPLOYMENT_TYPE="docker-compose"
    
    # Extract services and their configurations
    yq '.services | keys[]' docker-compose.yml > services.txt
    yq '.services[] | .ports[]?' docker-compose.yml 2>/dev/null > exposed_ports.txt
    yq '.services[] | .environment[]?' docker-compose.yml 2>/dev/null > env_vars.txt
  fi
  
  # Kubernetes deployment
  if [ -d "k8s" ] || [ -d "kubernetes" ] || fd "deployment\.ya?ml$" > /dev/null; then
    echo "☸️  Kubernetes deployment detected"
    DEPLOYMENT_TYPE="kubernetes"
    
    # Analyze K8s resources
    fd "\.ya?ml$" k8s/ kubernetes/ | xargs yq '.kind' 2>/dev/null | sort | uniq > k8s_resources.txt
    fd "\.ya?ml$" k8s/ kubernetes/ | xargs yq '.spec.ports[]?.port' 2>/dev/null > k8s_ports.txt
  fi
  
  # Database analysis
  if rg -q "postgresql|postgres|mysql|mongodb|redis|dragonfly" .; then
    echo "🗄️  Database dependencies detected"
    rg "postgresql|postgres|mysql|mongodb|redis|dragonfly" --type yaml --type json --type env \
      | cut -d: -f3 | sort | uniq > database_types.txt
  fi
  
  # External service dependencies
  rg "https?://[^/]+|api\.[^/]+" --type ts --type js --type go --type rust --type py \
    | rg -o "https?://[^/]+" | sort | uniq > external_services.txt
}

# Analyze API endpoints and attack surface
analyze_api_surface() {
  echo "🌐 Analyzing API attack surface..."
  
  case $DETECTED_LANGUAGE in
    "rust")
      # Axum/Actix routes
      rg "Router::new\(\)|\.route\(|\.get\(|\.post\(|\.put\(|\.delete\(" --type rust -A 2 -B 1 > api_routes.txt
      rg "#\[derive\(.*Serialize.*Deserialize.*\)\]|#\[serde" --type rust -A 5 > data_models.txt
      ;;
    "go") 
      # Gin/Echo/ConnectRPC routes
      rg "router\.(GET|POST|PUT|DELETE)|connect\.|http\.Handle" --type go -A 2 > api_routes.txt
      rg "type.*struct|json:\"|validate:" --type go -A 3 > data_models.txt
      ;;
    "typescript"|"javascript")
      # Express/Fastify/Fresh routes
      rg "(app|router)\.(get|post|put|delete)|export.*handler" --type ts --type js -A 2 > api_routes.txt
      rg "interface.*{|type.*=" --type ts -A 5 > data_models.txt
      ;;
    "java")
      # Spring Boot annotations
      rg "@(GetMapping|PostMapping|PutMapping|DeleteMapping|RequestMapping)" --type java -A 3 > api_routes.txt
      rg "@Entity|@Table|@Column" --type java -A 5 > data_models.txt
      ;;
  esac
}
```

### Security Context Analysis

**Existing Security Controls Discovery:**

```bash
# Analyze existing security implementations
analyze_security_controls() {
  echo "🔒 Analyzing existing security controls..."
  
  # Authentication mechanisms
  rg "jwt|token|auth|login|passport|oauth|saml|oidc" --ignore-case . \
    | head -20 > auth_mechanisms.txt
  
  # Authorization patterns  
  rg "role|permission|rbac|acl|authorize|admin|user" --ignore-case . \
    | head -20 > authz_patterns.txt
  
  # Input validation
  rg "validate|sanitize|escape|xss|sql.*injection|csrf" --ignore-case . \
    | head -20 > validation_controls.txt
  
  # Cryptography usage
  rg "encrypt|decrypt|hash|hmac|aes|rsa|bcrypt|scrypt|argon" --ignore-case . \
    | head -20 > crypto_usage.txt
  
  # Security headers and configurations
  rg "cors|csp|hsts|x-frame|x-content-type|security.*header" --ignore-case . \
    | head -20 > security_headers.txt
  
  # Secrets and configuration
  rg "secret|password|key|token" --type env --type yaml --type json \
    | head -20 > secrets_config.txt
}

# Network security analysis  
analyze_network_security() {
  echo "🌐 Analyzing network security configuration..."
  
  # TLS/SSL configuration
  if [ -d "nginx" ] || [ -d "apache" ] || fd "nginx\.conf|httpd\.conf" > /dev/null; then
    echo "🔐 Web server configuration detected"
    rg "ssl|tls|https|cert" nginx/ apache/ *.conf 2>/dev/null > tls_config.txt
  fi
  
  # Container security
  if [ -f "Dockerfile" ]; then
    echo "🐳 Dockerfile security analysis"
    rg "USER|EXPOSE|COPY|ADD|RUN.*sudo|chmod|chown" Dockerfile > container_security.txt
  fi
  
  # Infrastructure as Code security
  if fd "terraform|\.tf$" > /dev/null; then
    echo "🏗️ Terraform security analysis"
    rg "security_group|firewall|policy|encryption" *.tf **/*.tf 2>/dev/null > iac_security.txt
  fi
}
```

## STRIDE Threat Analysis

### 1. Systematic Threat Identification

**STRIDE Methodology Implementation:**

```typescript
// Generated STRIDE threat analysis engine
interface Component {
  id: string;
  name: string;
  type: "process" | "data_store" | "external_entity" | "data_flow";
  trustBoundary: string;
  technologies: string[];
  dataClassification: "public" | "internal" | "confidential" | "restricted";
}

interface ThreatVector {
  id: string;
  category: "S" | "T" | "R" | "I" | "D" | "E"; // STRIDE
  title: string;
  description: string;
  component: string;
  riskScore: number;
  likelihood: "low" | "medium" | "high";
  impact: "low" | "medium" | "high" | "critical";
  mitigations: Mitigation[];
  attackVectors: AttackVector[];
}

interface Mitigation {
  type: "preventive" | "detective" | "corrective";
  description: string;
  implemented: boolean;
  effort: "low" | "medium" | "high";
  effectiveness: "low" | "medium" | "high";
}

interface AttackVector {
  technique: string;
  complexity: "low" | "medium" | "high";
  prerequisites: string[];
  impact: string;
  mitreId?: string;
}

export class StrideAnalyzer {
  generateThreatModel(components: Component[]): ThreatVector[] {
    const threats: ThreatVector[] = [];

    for (const component of components) {
      threats.push(...this.analyzeSpoofing(component));
      threats.push(...this.analyzeTampering(component));
      threats.push(...this.analyzeRepudiation(component));
      threats.push(...this.analyzeInformationDisclosure(component));
      threats.push(...this.analyzeDenialOfService(component));
      threats.push(...this.analyzeElevationOfPrivilege(component));
    }

    return threats.sort((a, b) => b.riskScore - a.riskScore);
  }

  private analyzeSpoofing(component: Component): ThreatVector[] {
    const threats: ThreatVector[] = [];

    if (component.type === "process" || component.type === "external_entity") {
      threats.push({
        id: `${component.id}-spoofing-1`,
        category: "S",
        title: "Identity Spoofing",
        description: `Attacker impersonates ${component.name} to gain unauthorized access`,
        component: component.id,
        riskScore: this.calculateRiskScore("medium", "high"),
        likelihood: "medium",
        impact: "high",
        mitigations: [
          {
            type: "preventive",
            description: "Implement strong authentication (MFA, certificates)",
            implemented: this.checkAuthenticationExists(component),
            effort: "medium",
            effectiveness: "high",
          },
          {
            type: "detective",
            description: "Monitor and log authentication attempts",
            implemented: false,
            effort: "low",
            effectiveness: "medium",
          },
        ],
        attackVectors: [
          {
            technique: "Credential Stuffing",
            complexity: "low",
            prerequisites: ["Exposed login endpoint", "Weak password policy"],
            impact: "Account takeover",
            mitreId: "T1110.004",
          },
          {
            technique: "Session Hijacking",
            complexity: "medium",
            prerequisites: ["Unencrypted session tokens", "Network access"],
            impact: "Session impersonation",
            mitreId: "T1539",
          },
        ],
      });

      // API-specific spoofing threats
      if (component.technologies.includes("api")) {
        threats.push({
          id: `${component.id}-spoofing-2`,
          category: "S",
          title: "API Key Spoofing",
          description: "Attacker uses stolen or forged API keys",
          component: component.id,
          riskScore: this.calculateRiskScore("high", "medium"),
          likelihood: "high",
          impact: "medium",
          mitigations: [
            {
              type: "preventive",
              description: "Implement API key rotation and scoping",
              implemented: false,
              effort: "medium",
              effectiveness: "high",
            },
          ],
          attackVectors: [
            {
              technique: "API Key Theft",
              complexity: "low",
              prerequisites: ["Exposed API keys in code/logs"],
              impact: "Unauthorized API access",
            },
          ],
        });
      }
    }

    return threats;
  }

  private analyzeTampering(component: Component): ThreatVector[] {
    const threats: ThreatVector[] = [];

    if (component.type === "data_store" || component.type === "data_flow") {
      threats.push({
        id: `${component.id}-tampering-1`,
        category: "T",
        title: "Data Tampering",
        description: `Unauthorized modification of data in ${component.name}`,
        component: component.id,
        riskScore: this.calculateRiskScore("medium", "high"),
        likelihood: "medium",
        impact: "high",
        mitigations: [
          {
            type: "preventive",
            description: "Implement data integrity checks (hashing, digital signatures)",
            implemented: false,
            effort: "medium",
            effectiveness: "high",
          },
          {
            type: "detective",
            description: "Audit logging for all data modifications",
            implemented: false,
            effort: "low",
            effectiveness: "medium",
          },
        ],
        attackVectors: [
          {
            technique: "SQL Injection",
            complexity: "low",
            prerequisites: ["Unvalidated user input", "Dynamic SQL queries"],
            impact: "Database manipulation",
            mitreId: "T1190",
          },
        ],
      });
    }

    return threats;
  }

  private analyzeInformationDisclosure(component: Component): ThreatVector[] {
    const threats: ThreatVector[] = [];

    if (
      component.dataClassification === "confidential" ||
      component.dataClassification === "restricted"
    ) {
      threats.push({
        id: `${component.id}-disclosure-1`,
        category: "I",
        title: "Sensitive Data Exposure",
        description: `Unauthorized access to sensitive data in ${component.name}`,
        component: component.id,
        riskScore: this.calculateRiskScore("medium", "critical"),
        likelihood: "medium",
        impact: "critical",
        mitigations: [
          {
            type: "preventive",
            description: "Encrypt sensitive data at rest and in transit",
            implemented: false,
            effort: "medium",
            effectiveness: "high",
          },
          {
            type: "preventive",
            description: "Implement proper access controls and data classification",
            implemented: false,
            effort: "high",
            effectiveness: "high",
          },
        ],
        attackVectors: [
          {
            technique: "Database Breach",
            complexity: "medium",
            prerequisites: ["Database access", "Unencrypted sensitive data"],
            impact: "Data exfiltration",
          },
        ],
      });
    }

    return threats;
  }

  private calculateRiskScore(likelihood: string, impact: string): number {
    const likelihoodScore = { low: 1, medium: 2, high: 3 };
    const impactScore = { low: 1, medium: 2, high: 3, critical: 4 };

    return (likelihoodScore[likelihood] || 1) * (impactScore[impact] || 1);
  }
}
```

### 2. Attack Surface Mapping

**Comprehensive Attack Vector Analysis:**

```typescript
// Generated attack surface analyzer
interface AttackSurface {
  endpoints: ApiEndpoint[];
  dataSources: DataSource[];
  externalDependencies: ExternalDependency[];
  networkExposure: NetworkExposure[];
  privilegedOperations: PrivilegedOperation[];
}

interface ApiEndpoint {
  path: string;
  method: string;
  authentication: boolean;
  authorization: string[];
  inputValidation: boolean;
  rateLimit: boolean;
  exposedData: string[];
  riskLevel: "low" | "medium" | "high" | "critical";
}

export class AttackSurfaceAnalyzer {
  async analyzeAttackSurface(): Promise<AttackSurface> {
    console.log("🎯 Analyzing attack surface...");

    const endpoints = await this.discoverApiEndpoints();
    const dataSources = await this.analyzeDataSources();
    const externalDeps = await this.analyzeExternalDependencies();
    const networkExposure = await this.analyzeNetworkExposure();
    const privilegedOps = await this.analyzePrivilegedOperations();

    return {
      endpoints,
      dataSources,
      externalDependencies: externalDeps,
      networkExposure,
      privilegedOperations: privilegedOps,
    };
  }

  private async discoverApiEndpoints(): Promise<ApiEndpoint[]> {
    const endpoints: ApiEndpoint[] = [];

    // Analyze route definitions
    const routeFiles = await this.findFiles(["**/*route*", "**/*handler*", "**/*controller*"]);

    for (const file of routeFiles) {
      const content = await Deno.readTextFile(file);

      // Extract HTTP methods and paths
      const httpMethods = content.match(/(GET|POST|PUT|DELETE|PATCH)\s+["']([^"']+)["']/g) || [];

      for (const match of httpMethods) {
        const [, method, path] = match.match(/(GET|POST|PUT|DELETE|PATCH)\s+["']([^"']+)["']/) ||
          [];

        if (method && path) {
          const hasAuth = this.checkAuthentication(content, path);
          const hasValidation = this.checkInputValidation(content, path);
          const hasRateLimit = this.checkRateLimit(content, path);

          endpoints.push({
            path,
            method,
            authentication: hasAuth,
            authorization: this.extractAuthorizationRoles(content, path),
            inputValidation: hasValidation,
            rateLimit: hasRateLimit,
            exposedData: this.extractExposedData(content, path),
            riskLevel: this.calculateEndpointRisk(path, method, hasAuth, hasValidation),
          });
        }
      }
    }

    return endpoints;
  }

  private calculateEndpointRisk(
    path: string,
    method: string,
    hasAuth: boolean,
    hasValidation: boolean,
  ): "low" | "medium" | "high" | "critical" {
    let riskScore = 0;

    // Path-based risk factors
    if (path.includes("/admin/") || path.includes("/internal/")) riskScore += 3;
    if (path.includes("/user/") || path.includes("/account/")) riskScore += 2;
    if (path.includes("/public/") || path.includes("/health/")) riskScore -= 1;

    // Method-based risk factors
    if (["POST", "PUT", "DELETE", "PATCH"].includes(method)) riskScore += 2;
    if (method === "GET") riskScore += 1;

    // Security control factors
    if (!hasAuth) riskScore += 3;
    if (!hasValidation) riskScore += 2;

    if (riskScore >= 7) return "critical";
    if (riskScore >= 5) return "high";
    if (riskScore >= 3) return "medium";
    return "low";
  }
}
```

## Risk Assessment and Prioritization

### 1. Quantitative Risk Analysis

**Risk Scoring Matrix:**

```typescript
// Generated risk assessment engine
interface RiskAssessment {
  threatId: string;
  businessImpact: BusinessImpact;
  technicalImpact: TechnicalImpact;
  exploitability: Exploitability;
  overallRisk: RiskLevel;
  priorityScore: number;
}

interface BusinessImpact {
  financialLoss: "none" | "minor" | "moderate" | "significant" | "catastrophic";
  reputationDamage: "none" | "minor" | "moderate" | "significant" | "catastrophic";
  regulatoryCompliance: "none" | "minor" | "moderate" | "significant" | "catastrophic";
  operationalDisruption: "none" | "minor" | "moderate" | "significant" | "catastrophic";
}

interface TechnicalImpact {
  dataConfidentiality: "none" | "low" | "medium" | "high";
  dataIntegrity: "none" | "low" | "medium" | "high";
  systemAvailability: "none" | "low" | "medium" | "high";
  accountability: "none" | "low" | "medium" | "high";
}

interface Exploitability {
  attackerSkill: "none" | "low" | "medium" | "high";
  motivation: "low" | "medium" | "high";
  opportunity: "none" | "low" | "medium" | "high";
  size:
    | "developers"
    | "system_administrators"
    | "intranet_users"
    | "partners"
    | "authenticated_users"
    | "anonymous_internet_users";
}

export class RiskCalculator {
  calculateRisk(threat: ThreatVector, context: SecurityContext): RiskAssessment {
    const businessImpact = this.assessBusinessImpact(threat, context);
    const technicalImpact = this.assessTechnicalImpact(threat);
    const exploitability = this.assessExploitability(threat, context);

    const overallRisk = this.calculateOverallRisk(businessImpact, technicalImpact, exploitability);
    const priorityScore = this.calculatePriorityScore(overallRisk, threat, context);

    return {
      threatId: threat.id,
      businessImpact,
      technicalImpact,
      exploitability,
      overallRisk,
      priorityScore,
    };
  }

  private assessBusinessImpact(threat: ThreatVector, context: SecurityContext): BusinessImpact {
    // Industry-specific impact assessment
    const industry = context.industry || "general";
    const dataTypes = context.dataTypes || [];

    let financialLoss: BusinessImpact["financialLoss"] = "minor";
    let reputationDamage: BusinessImpact["reputationDamage"] = "minor";
    let regulatoryCompliance: BusinessImpact["regulatoryCompliance"] = "none";
    let operationalDisruption: BusinessImpact["operationalDisruption"] = "minor";

    // Data-driven impact assessment
    if (dataTypes.includes("pii") || dataTypes.includes("financial")) {
      financialLoss = "significant";
      reputationDamage = "significant";
      regulatoryCompliance = "significant";
    }

    if (dataTypes.includes("healthcare")) {
      regulatoryCompliance = "catastrophic"; // HIPAA implications
      reputationDamage = "significant";
    }

    // Industry-specific adjustments
    if (industry === "financial_services") {
      financialLoss = "catastrophic";
      regulatoryCompliance = "catastrophic";
    }

    // Threat category adjustments
    if (threat.category === "D") { // Denial of Service
      operationalDisruption = "significant";
    }

    if (threat.category === "I") { // Information Disclosure
      reputationDamage = "significant";
    }

    return { financialLoss, reputationDamage, regulatoryCompliance, operationalDisruption };
  }

  private calculateOverallRisk(
    business: BusinessImpact,
    technical: TechnicalImpact,
    exploit: Exploitability,
  ): RiskLevel {
    const businessScore = this.scoreBusinessImpact(business);
    const technicalScore = this.scoreTechnicalImpact(technical);
    const exploitScore = this.scoreExploitability(exploit);

    const totalScore = (businessScore + technicalScore + exploitScore) / 3;

    if (totalScore >= 8) return "critical";
    if (totalScore >= 6) return "high";
    if (totalScore >= 4) return "medium";
    return "low";
  }
}
```

### 2. Mitigation Strategy Generation

**Automated Mitigation Planning:**

```typescript
// Generated mitigation strategy engine
interface MitigationPlan {
  threatId: string;
  strategies: MitigationStrategy[];
  implementation: ImplementationPlan;
  costBenefit: CostBenefitAnalysis;
}

interface MitigationStrategy {
  type: "eliminate" | "reduce" | "transfer" | "accept";
  controls: SecurityControl[];
  effectiveness: number; // 0-100%
  residualRisk: RiskLevel;
}

interface SecurityControl {
  id: string;
  name: string;
  category: "preventive" | "detective" | "corrective" | "deterrent";
  implementation: "technical" | "administrative" | "physical";
  effort: EstimatedEffort;
  dependencies: string[];
  codeExample?: string;
  configExample?: string;
}

export class MitigationPlanner {
  generateMitigationPlan(threat: ThreatVector, riskAssessment: RiskAssessment): MitigationPlan {
    const strategies = this.generateStrategies(threat);
    const implementation = this.createImplementationPlan(strategies);
    const costBenefit = this.analyzeCostBenefit(strategies, riskAssessment);

    return {
      threatId: threat.id,
      strategies,
      implementation,
      costBenefit,
    };
  }

  private generateStrategies(threat: ThreatVector): MitigationStrategy[] {
    const strategies: MitigationStrategy[] = [];

    // STRIDE-specific mitigation strategies
    switch (threat.category) {
      case "S": // Spoofing
        strategies.push({
          type: "reduce",
          controls: [
            {
              id: "auth-mfa",
              name: "Multi-Factor Authentication",
              category: "preventive",
              implementation: "technical",
              effort: { hours: 16, complexity: "medium" },
              dependencies: ["identity-provider"],
              codeExample: this.generateMFACode(threat.component),
            },
            {
              id: "auth-cert",
              name: "Certificate-Based Authentication",
              category: "preventive",
              implementation: "technical",
              effort: { hours: 24, complexity: "high" },
              dependencies: ["pki-infrastructure"],
            },
          ],
          effectiveness: 85,
          residualRisk: "low",
        });
        break;

      case "T": // Tampering
        strategies.push({
          type: "reduce",
          controls: [
            {
              id: "input-validation",
              name: "Input Validation and Sanitization",
              category: "preventive",
              implementation: "technical",
              effort: { hours: 8, complexity: "low" },
              dependencies: [],
              codeExample: this.generateValidationCode(threat.component),
            },
            {
              id: "data-integrity",
              name: "Data Integrity Checks",
              category: "detective",
              implementation: "technical",
              effort: { hours: 12, complexity: "medium" },
              dependencies: [],
              codeExample: this.generateIntegrityCode(threat.component),
            },
          ],
          effectiveness: 90,
          residualRisk: "low",
        });
        break;

      case "I": // Information Disclosure
        strategies.push({
          type: "reduce",
          controls: [
            {
              id: "encryption-rest",
              name: "Encryption at Rest",
              category: "preventive",
              implementation: "technical",
              effort: { hours: 20, complexity: "medium" },
              dependencies: ["key-management"],
              codeExample: this.generateEncryptionCode(threat.component),
            },
            {
              id: "access-control",
              name: "Role-Based Access Control",
              category: "preventive",
              implementation: "technical",
              effort: { hours: 32, complexity: "high" },
              dependencies: ["identity-management"],
            },
          ],
          effectiveness: 80,
          residualRisk: "medium",
        });
        break;
    }

    return strategies;
  }

  private generateMFACode(component: string): string {
    return `
// Multi-Factor Authentication Implementation
import { TOTP } from "otplib";

export class MFAService {
  async verifyMFA(userId: string, token: string, secret: string): Promise<boolean> {
    try {
      // Verify TOTP token
      const isValid = TOTP.verify({ token, secret });
      
      if (isValid) {
        await this.logMFASuccess(userId);
        return true;
      } else {
        await this.logMFAFailure(userId);
        return false;
      }
    } catch (error) {
      await this.logMFAError(userId, error);
      return false;
    }
  }
  
  async setupMFA(userId: string): Promise<{ secret: string; qrCode: string }> {
    const secret = TOTP.generateSecret();
    const qrCode = await this.generateQRCode(userId, secret);
    
    // Store secret securely (encrypted)
    await this.storeEncryptedSecret(userId, secret);
    
    return { secret, qrCode };
  }
}`;
  }

  private generateValidationCode(component: string): string {
    return `
// Input Validation and Sanitization
import { z } from "zod";
import DOMPurify from "dompurify";

export class InputValidator {
  // Schema-based validation
  private userSchema = z.object({
    email: z.string().email().max(254),
    name: z.string().min(1).max(100).regex(/^[a-zA-Z\s]+$/),
    age: z.number().int().min(0).max(150)
  });
  
  validateUser(input: unknown): { valid: boolean; data?: any; errors?: string[] } {
    try {
      const data = this.userSchema.parse(input);
      return { valid: true, data };
    } catch (error) {
      if (error instanceof z.ZodError) {
        return { 
          valid: false, 
          errors: error.errors.map(e => \`\${e.path.join('.')}: \${e.message}\`)
        };
      }
      return { valid: false, errors: ['Invalid input format'] };
    }
  }
  
  // XSS Prevention
  sanitizeHTML(input: string): string {
    return DOMPurify.sanitize(input, { 
      ALLOWED_TAGS: ['b', 'i', 'em', 'strong'],
      ALLOWED_ATTR: []
    });
  }
  
  // SQL Injection Prevention (use parameterized queries)
  async executeQuery(query: string, params: any[]): Promise<any> {
    // Always use parameterized queries
    return await this.db.execute(query, params);
  }
}`;
  }
}
```

## Compliance and Standards Integration

### 1. Regulatory Framework Mapping

**Compliance Assessment:**

```typescript
// Generated compliance analyzer
interface ComplianceFramework {
  name: string;
  requirements: ComplianceRequirement[];
  applicability: string[];
}

interface ComplianceRequirement {
  id: string;
  title: string;
  description: string;
  threatCategories: string[];
  controls: string[];
  auditEvidence: string[];
}

export class ComplianceAnalyzer {
  private frameworks: ComplianceFramework[] = [
    {
      name: "GDPR",
      requirements: [
        {
          id: "GDPR-32",
          title: "Security of Processing",
          description: "Implement appropriate technical and organizational measures",
          threatCategories: ["I", "T"],
          controls: ["encryption", "access-control", "audit-logging"],
          auditEvidence: ["encryption-policy", "access-logs", "security-assessments"],
        },
      ],
      applicability: ["personal-data", "eu-operations"],
    },
    {
      name: "SOX",
      requirements: [
        {
          id: "SOX-404",
          title: "Internal Controls over Financial Reporting",
          description: "Maintain adequate internal control structure",
          threatCategories: ["T", "R"],
          controls: ["change-management", "segregation-duties", "audit-trails"],
          auditEvidence: ["change-logs", "approval-workflows", "audit-reports"],
        },
      ],
      applicability: ["financial-data", "public-company"],
    },
  ];

  assessCompliance(threats: ThreatVector[], context: SecurityContext): ComplianceGap[] {
    const gaps: ComplianceGap[] = [];

    for (const framework of this.frameworks) {
      if (this.isFrameworkApplicable(framework, context)) {
        for (const requirement of framework.requirements) {
          const gap = this.assessRequirement(requirement, threats);
          if (gap) {
            gaps.push({
              framework: framework.name,
              requirement: requirement.id,
              ...gap,
            });
          }
        }
      }
    }

    return gaps;
  }
}
```

## Report Generation and Visualization

### 1. Executive Summary Report

**Comprehensive Threat Model Report:**

```typescript
// Generated report generator
export class ThreatModelReporter {
  generateExecutiveReport(
    threats: ThreatVector[],
    riskAssessments: RiskAssessment[],
    mitigationPlans: MitigationPlan[],
  ): string {
    const criticalThreats = threats.filter((t) =>
      riskAssessments.find((r) => r.threatId === t.id)?.overallRisk === "critical"
    );
    const totalRiskScore = riskAssessments.reduce((sum, r) => sum + r.priorityScore, 0);

    return `
# Threat Model Assessment Report

## Executive Summary

**Assessment Date:** ${new Date().toISOString().split("T")[0]}
**Total Threats Identified:** ${threats.length}
**Critical Risk Threats:** ${criticalThreats.length}
**Overall Risk Score:** ${totalRiskScore}

### Key Findings

${
      criticalThreats.slice(0, 5).map((threat) => `
- **${threat.title}** (${threat.category})
  - Risk Level: Critical
  - Impact: ${threat.impact}
  - Mitigation Status: ${
        threat.mitigations.filter((m) => m.implemented).length
      }/${threat.mitigations.length} controls implemented
`).join("")
    }

### Risk Distribution

| Risk Level | Count | Percentage |
|------------|-------|------------|
| Critical   | ${riskAssessments.filter((r) => r.overallRisk === "critical").length} | ${
      ((riskAssessments.filter((r) => r.overallRisk === "critical").length /
        riskAssessments.length) * 100).toFixed(1)
    }% |
| High       | ${riskAssessments.filter((r) => r.overallRisk === "high").length} | ${
      ((riskAssessments.filter((r) => r.overallRisk === "high").length / riskAssessments.length) *
        100).toFixed(1)
    }% |
| Medium     | ${riskAssessments.filter((r) => r.overallRisk === "medium").length} | ${
      ((riskAssessments.filter((r) => r.overallRisk === "medium").length / riskAssessments.length) *
        100).toFixed(1)
    }% |
| Low        | ${riskAssessments.filter((r) => r.overallRisk === "low").length} | ${
      ((riskAssessments.filter((r) => r.overallRisk === "low").length / riskAssessments.length) *
        100).toFixed(1)
    }% |

### Immediate Actions Required

${this.generateActionItems(criticalThreats, mitigationPlans)}

### Investment Priorities

${this.generateInvestmentPriorities(mitigationPlans)}

## Detailed Assessment

${
      threats.map((threat) => this.generateThreatDetail(threat, riskAssessments, mitigationPlans))
        .join("\n\n")
    }
`;
  }

  private generateActionItems(threats: ThreatVector[], plans: MitigationPlan[]): string {
    const urgentActions = plans
      .filter((p) => threats.find((t) => t.id === p.threatId)?.impact === "critical")
      .flatMap((p) => p.strategies.flatMap((s) => s.controls))
      .filter((c) => c.effort.complexity === "low")
      .slice(0, 5);

    return urgentActions.map((action) =>
      `1. **${action.name}** - ${action.effort.hours} hours (${action.implementation})`
    ).join("\n");
  }
}
```

## Integration and Output

### Integration with Other Commands

- Use with `/audit` for comprehensive security assessment
- Combine with `/harden` to implement identified mitigations
- Integrate with `/ci-gen` for automated threat model validation
- Use with `/monitor` to track threat landscape changes

### Generated Outputs

1. **STRIDE Threat Analysis**: Systematic threat identification using proven methodology
2. **Risk Assessment Matrix**: Quantitative risk scoring and prioritization
3. **Attack Surface Map**: Comprehensive analysis of potential attack vectors
4. **Mitigation Strategies**: Specific, actionable security controls with code examples
5. **Compliance Mapping**: Regulatory requirement alignment and gap analysis
6. **Executive Report**: Business-focused threat model summary and recommendations
